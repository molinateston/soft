#!/usr/bin/env python3
"""Instala sozinho o ambiente das skills de edição de vídeo (Linux, Mac e Windows).

Uso:
  python3 instalar_ambiente.py --perfil hyperframes --pasta <pasta de trabalho>
  python3 instalar_ambiente.py --perfil ffmpeg --pasta <pasta de trabalho> [--simular]

Perfis:
  hyperframes  node 22+, npm, hyperframes@0.8.93 e gsap@3.14.2 na pasta, Chrome do render,
               ffmpeg e ffprobe, venv com faster-whisper, tesseract (opcional)
  ffmpeg       ffmpeg e ffprobe, venv com faster-whisper

O que não exige privilégio fica dentro da pasta (node baixado em .ambiente/node, ffmpeg estático
em .ambiente/bin, venv em .ambiente/venv, pacotes npm em node_modules). O que exige privilégio e
não houver vira um comando exato para o dono rodar (saída 3).

Saídas: 0 pronto, 1 conferência reprovou, 2 argumento errado, 3 falta algo que só o dono faz,
4 uma instalação falhou. Só usa a biblioteca padrão do python.
"""
import argparse, gzip, hashlib, json, os, platform, re, shutil, socket, stat, subprocess, sys, tarfile, time, urllib.request, zipfile
from pathlib import Path

VERSOES = {
    "node_minimo": 22,
    "node_local": "22.22.2",
    "hyperframes": "0.8.93",
    "gsap": "3.14.2",
    "ffmpeg_estatico": "b6.1.1",  # mesma release que o pacote npm ffmpeg-static 5.3.0 baixa
    "python_minimo": (3, 10),
    "pip_fixado": ["faster-whisper==1.2.1", "ctranslate2==4.7.2", "av==17.0.1"],
    "pip_reserva": ["faster-whisper==1.2.1", "av<19"],  # av 19 quebra o faster-whisper 1.2.1
}
URL_NODE = "https://nodejs.org/dist/v{v}/"
URL_FF = "https://github.com/eugeneware/ffmpeg-static/releases/download/{tag}/{arq}"
URL_GETPIP = "https://bootstrap.pypa.io/get-pip.py"
WIN = os.name == "nt"
EXE = ".exe" if WIN else ""

# so faltante do Chrome -> (pacotes apt candidatos, pacote dnf)
LIBS_CHROME = {
    "libglib-2.0.so.0": (["libglib2.0-0t64", "libglib2.0-0"], "glib2"),
    "libgobject-2.0.so.0": (["libglib2.0-0t64", "libglib2.0-0"], "glib2"),
    "libgio-2.0.so.0": (["libglib2.0-0t64", "libglib2.0-0"], "glib2"),
    "libgmodule-2.0.so.0": (["libglib2.0-0t64", "libglib2.0-0"], "glib2"),
    "libnspr4.so": (["libnspr4"], "nspr"), "libplc4.so": (["libnspr4"], "nspr"), "libplds4.so": (["libnspr4"], "nspr"),
    "libnss3.so": (["libnss3"], "nss"), "libnssutil3.so": (["libnss3"], "nss-util"),
    "libatk-1.0.so.0": (["libatk1.0-0t64", "libatk1.0-0"], "atk"),
    "libatk-bridge-2.0.so.0": (["libatk-bridge2.0-0t64", "libatk-bridge2.0-0"], "at-spi2-atk"),
    "libatspi.so.0": (["libatspi2.0-0t64", "libatspi2.0-0"], "at-spi2-core"),
    "libdbus-1.so.3": (["libdbus-1-3"], "dbus-libs"),
    "libX11.so.6": (["libx11-6"], "libX11"), "libXcomposite.so.1": (["libxcomposite1"], "libXcomposite"),
    "libXdamage.so.1": (["libxdamage1"], "libXdamage"), "libXext.so.6": (["libxext6"], "libXext"),
    "libXfixes.so.3": (["libxfixes3"], "libXfixes"), "libXrandr.so.2": (["libxrandr2"], "libXrandr"),
    "libXrender.so.1": (["libxrender1"], "libXrender"), "libXi.so.6": (["libxi6"], "libXi"),
    "libgbm.so.1": (["libgbm1"], "mesa-libgbm"), "libexpat.so.1": (["libexpat1"], "expat"),
    "libxcb.so.1": (["libxcb1"], "libxcb"), "libxkbcommon.so.0": (["libxkbcommon0"], "libxkbcommon"),
    "libudev.so.1": (["libudev1"], "systemd-libs"), "libasound.so.2": (["libasound2t64", "libasound2"], "alsa-lib"),
    "libdrm.so.2": (["libdrm2"], "libdrm"), "libatomic.so.1": (["libatomic1"], "libatomic"),
    "libcups.so.2": (["libcups2t64", "libcups2"], "cups-libs"),
    "libpango-1.0.so.0": (["libpango-1.0-0"], "pango"), "libcairo.so.2": (["libcairo2"], "cairo"),
}
PACOTES_SISTEMA = {  # gerenciador -> item -> pacotes
    "apt": {"ffmpeg": ["ffmpeg"], "venv": ["python3-venv"], "tesseract": ["tesseract-ocr", "tesseract-ocr-por"], "fontes": ["fonts-dejavu-core"]},
    "dnf": {"ffmpeg": ["ffmpeg"], "venv": ["python3-virtualenv"], "tesseract": ["tesseract", "tesseract-langpack-por"], "fontes": ["dejavu-sans-fonts"]},
    "brew": {"ffmpeg": ["ffmpeg"], "venv": ["python"], "tesseract": ["tesseract", "tesseract-lang"], "fontes": []},
    "winget": {"ffmpeg": ["Gyan.FFmpeg"], "venv": ["Python.Python.3.12"], "tesseract": ["UB-Mannheim.TesseractOCR"], "fontes": []},
    "choco": {"ffmpeg": ["ffmpeg"], "venv": ["python"], "tesseract": ["tesseract"], "fontes": []},
}


class Saida(Exception):
    def __init__(self, codigo, msg=""):
        super().__init__(msg)
        self.codigo, self.msg = codigo, msg


class ParserPt(argparse.ArgumentParser):
    def error(self, message):
        traduz = {"the following arguments are required": "faltam os argumentos", "invalid choice": "opção inválida",
                  "unrecognized arguments": "argumentos desconhecidos", "expected one argument": "esperava um valor", "choose from": "escolha entre", "argument ": "argumento "}
        for en, pt in traduz.items():
            message = message.replace(en, pt)
        sys.stderr.write(f"argumento errado: {message}\n\n{self.format_usage().replace('usage:', 'uso:')}")
        sys.exit(2)


# ---------------------------------------------------------------- utilidades
def rodar(cmd, env=None, cwd=None, log=None, timeout=None):
    """Roda um comando; devolve (código, saída). Com log, grava a saída inteira no arquivo."""
    try:
        r = subprocess.run(cmd, env=env, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           text=True, encoding="utf-8", errors="replace", timeout=timeout,
                           shell=isinstance(cmd, str))
        out = r.stdout or ""
        rc = r.returncode
    except (OSError, subprocess.TimeoutExpired) as e:
        out, rc = str(e), 127
    if log:
        Path(log).parent.mkdir(parents=True, exist_ok=True)
        with open(log, "a", encoding="utf-8") as f:
            f.write(f"$ {cmd if isinstance(cmd, str) else ' '.join(map(str, cmd))}\n{out}\n[saída {rc}]\n\n")
    return rc, out


def mostra_cmd(cmd):
    if isinstance(cmd, str):
        return cmd
    return " ".join(f'"{c}"' if any(x in str(c) for x in " <>&|") else str(c) for c in cmd)


def baixar(url, destino, timeout=60):
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    tmp = destino.with_name(destino.name + ".parcial")
    req = urllib.request.Request(url, headers={"User-Agent": "instalar-ambiente-soft"})
    total = 0
    with urllib.request.urlopen(req, timeout=timeout) as r, open(tmp, "wb") as f:
        while True:
            bloco = r.read(1 << 20)
            if not bloco:
                break
            f.write(bloco)
            total += len(bloco)
    tmp.replace(destino)
    return total


def sha256(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def versao_tupla(txt):
    return tuple(int(x) for x in re.findall(r"\d+", txt)[:3])


# ---------------------------------------------------------------- detecção do sistema
def detectar_sistema(args, pasta):
    so = {"Linux": "linux", "Darwin": "mac", "Windows": "windows"}.get(platform.system(), platform.system().lower())
    maq = platform.machine().lower()
    arch = {"x86_64": "x64", "amd64": "x64", "aarch64": "arm64", "arm64": "arm64", "i386": "ia32", "i686": "ia32", "armv7l": "arm"}.get(maq, maq)
    gerenciador = next((g for g, b in [("apt", "apt-get"), ("dnf", "dnf"), ("brew", "brew"), ("winget", "winget"), ("choco", "choco")] if shutil.which(b)), None)
    if args.sem_privilegio:
        priv = "nenhum (pedido com --sem-privilegio)"
    elif WIN:
        try:
            import ctypes
            priv = "administrador" if ctypes.windll.shell32.IsUserAnAdmin() else "nenhum"
        except Exception:
            priv = "nenhum"
    elif os.geteuid() == 0:
        priv = "root"
    elif shutil.which("sudo") and rodar(["sudo", "-n", "true"], timeout=10)[0] == 0:
        priv = "sudo sem senha"
    elif gerenciador == "brew":
        priv = "brew (sem sudo)"
    else:
        priv = "nenhum"
    rede = {}
    for host in ["registry.npmjs.org", "pypi.org", "github.com", "nodejs.org", "storage.googleapis.com"]:
        try:
            socket.create_connection((host, 443), timeout=5).close()
            rede[host] = True
        except OSError:
            rede[host] = bool(os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy"))  # com proxy, tenta mesmo assim
    base = pasta if pasta.exists() else pasta.parent
    while not base.exists():
        base = base.parent
    livre = round(shutil.disk_usage(base).free / 1e9, 1)
    return {"so": so, "arch": arch, "versao_so": platform.platform(terse=True), "gerenciador": gerenciador or "nenhum",
            "privilegio": priv, "pode_privilegio": not priv.startswith("nenhum"), "rede": rede, "disco_livre_gb": livre,
            "python": platform.python_version()}


def comando_sistema(sis, chave, pacotes=None):
    """Comando exato de instalação de pacote de sistema, ou None se não houver gerenciador conhecido."""
    g = sis["gerenciador"]
    if g not in PACOTES_SISTEMA:
        return None
    pk = pacotes if pacotes is not None else PACOTES_SISTEMA[g].get(chave, [])
    if not pk:
        return None
    s = "" if sis["privilegio"] in ("root",) or g in ("brew", "winget", "choco") else "sudo "
    if g == "apt":
        return f"{s}apt-get update && {s}env DEBIAN_FRONTEND=noninteractive apt-get install -y {' '.join(pk)}"
    if g == "dnf":
        return f"{s}dnf install -y {' '.join(pk)}"
    if g == "brew":
        return f"brew install {' '.join(pk)}"
    if g == "winget":
        return " && ".join(f"winget install -e --id {p} --accept-source-agreements --accept-package-agreements" for p in pk)
    if g == "choco":
        return f"choco install -y {' '.join(pk)}"
    return None


def comando_dono(cmd):
    """Para o dono: sempre com sudo quando é apt ou dnf (ele roda como administrador)."""
    if cmd and not cmd.startswith(("sudo", "brew", "winget", "choco")) and ("apt-get" in cmd or "dnf " in cmd):
        return "sudo " + cmd.replace(" && env ", " && sudo env ").replace("&& apt-get", "&& sudo apt-get")
    return cmd


# ---------------------------------------------------------------- o instalador
class Instalador:
    def __init__(self, args):
        self.args = args
        self.pasta = Path(args.pasta).expanduser().resolve()
        self.amb = self.pasta / ".ambiente"
        self.logs = self.amb / "logs"
        self.simular = args.simular
        self.perfil = args.perfil
        self.linhas = []  # (item, estado, detalhe)
        self.dono = []  # (motivo, comando)
        self.feitos = []  # (descrição, segundos)
        self.planos = []  # comandos que rodaria (modo simular)
        self.info = {}
        self.sis = detectar_sistema(args, self.pasta)
        self.path_extra = []

    # ---------- ambiente dos subprocessos
    def env(self):
        e = dict(os.environ)
        extra = [str(p) for p in self.path_extra]
        if extra:
            e["PATH"] = os.pathsep.join(extra + [e.get("PATH", "")])
        e.update({"HYPERFRAMES_NO_TELEMETRY": "1", "HYPERFRAMES_NO_UPDATE_CHECK": "1", "npm_config_update_notifier": "false",
                  "npm_config_fund": "false", "npm_config_audit": "false", "PIP_DISABLE_PIP_VERSION_CHECK": "1"})
        return e

    def which(self, nome):
        return shutil.which(nome, path=self.env()["PATH"])

    def precisa_rede(self, host, o_que):
        if not self.sis["rede"].get(host, False):
            self.dono.append((f"sem acesso a {host} para baixar {o_que}", f"libere a saída HTTPS para {host} (porta 443) e rode o instalador de novo"))
            return False
        return True

    def executar(self, descricao, cmd, nome_log, cwd=None, timeout=1800):
        """Executa um passo (ou só o anuncia no modo simular). Falha vira saída 4."""
        if self.simular:
            self.planos.append((descricao, mostra_cmd(cmd)))
            return ""
        print(f"  instalando: {descricao}", flush=True)
        t = time.time()
        rc, out = rodar(cmd, env=self.env(), cwd=cwd, log=self.logs / f"{nome_log}.log", timeout=timeout)
        dt = time.time() - t
        if rc != 0:
            cauda = "\n".join(out.strip().splitlines()[-15:])
            raise Saida(4, f"falhou: {descricao} (saída {rc}, {dt:.0f} s)\ncomando: {mostra_cmd(cmd)}\nlog completo: {self.logs / (nome_log + '.log')}\nfinal do log:\n{cauda}")
        self.feitos.append((descricao, round(dt, 1)))
        print(f"    ok em {dt:.0f} s", flush=True)
        return out

    def passo_python(self, descricao, func, mostra="(download feito pelo próprio instalador)"):
        """Passo feito em python (download): no simular só anuncia."""
        if self.simular:
            self.planos.append((descricao, mostra))
            return None
        print(f"  instalando: {descricao}", flush=True)
        t = time.time()
        try:
            r = func()
        except Saida:
            raise
        except Exception as e:
            raise Saida(4, f"falhou: {descricao}: {e}")
        dt = time.time() - t
        self.feitos.append((descricao, round(dt, 1)))
        print(f"    ok em {dt:.0f} s", flush=True)
        return r

    def privilegiado(self, motivo, cmd, nome_log):
        """Passo de sistema: roda se houver privilégio, senão vira pedido ao dono. Devolve True se rodou."""
        if not cmd:
            self.dono.append((motivo, "instale manualmente: não achei gerenciador de pacotes conhecido (apt, dnf, brew, winget, choco)"))
            return False
        if not self.sis["pode_privilegio"]:
            self.dono.append((motivo, comando_dono(cmd)))
            return False
        self.executar(motivo, cmd, nome_log)
        return True

    # ---------- conferências (sem efeito colateral)
    def conf_node(self):
        local = self.amb / "node" / ("node.exe" if WIN else "bin/node")
        for cand in ([str(local)] if local.exists() else []) + [self.which("node")]:
            if not cand:
                continue
            rc, out = rodar([cand, "-p", "process.versions.node"], timeout=30)
            if rc == 0:
                v = out.strip().splitlines()[-1]
                return {"caminho": cand, "versao": v, "ok": versao_tupla(v)[0] >= VERSOES["node_minimo"],
                        "origem": "local" if cand == str(local) else "sistema"}
        return None

    def npm_cmd(self, node):
        n = Path(node).resolve()
        for cli in [n.parent / "node_modules/npm/bin/npm-cli.js", n.parent.parent / "lib/node_modules/npm/bin/npm-cli.js",
                    Path("/usr/share/nodejs/npm/bin/npm-cli.js")]:
            if cli.exists():
                return [str(n), str(cli)]
        w = self.which("npm")
        return [w] if w else None

    def conf_ff(self, nome):
        locais = self.amb / "bin" / f"{nome}{EXE}"
        cands = [str(locais)] if locais.exists() else []
        if not self.args.so_ffmpeg_local and self.which(nome):
            cands.insert(0, self.which(nome))
        for c in cands:
            rc, out = rodar([c, "-hide_banner", "-version"], timeout=30)
            if rc != 0:
                continue
            v = re.search(rf"{nome} version (\S+)", out)
            d = {"caminho": c, "versao": v.group(1) if v else "?", "origem": "local" if c == str(locais) else "sistema", "ok": True}
            if nome == "ffmpeg":
                rc2, enc = rodar([c, "-hide_banner", "-encoders"], timeout=30)
                faltam = [e for e in ("libx264", "aac") if not re.search(rf"\s{e}\s", enc)]
                if faltam:
                    d.update(ok=False, motivo=f"sem os codificadores {', '.join(faltam)}")
                    continue
            return d
        return None

    def conf_pacote_npm(self, nome):
        pj = self.pasta / "node_modules" / nome / "package.json"
        try:
            return json.loads(pj.read_text(encoding="utf-8"))["version"]
        except Exception:
            return None

    def hf_bin(self):
        return self.pasta / "node_modules" / "hyperframes" / "bin" / "hyperframes.mjs"

    def conf_navegador(self, node):
        if not node or not self.hf_bin().exists():
            return None
        rc, out = rodar([node, str(self.hf_bin()), "browser", "path"], env=self.env(), cwd=self.pasta, timeout=60)
        linhas = [l.strip() for l in out.splitlines() if l.strip() and os.path.isabs(l.strip())]
        if rc == 0 and linhas and Path(linhas[-1]).exists():
            p = linhas[-1]
            return {"caminho": p, "headless": Path(p).name.lower().startswith("chrome-headless-shell")}
        return None

    def libs_faltando(self, navegador):
        if self.sis["so"] != "linux" or not shutil.which("ldd"):
            return []
        rc, out = rodar(["ldd", navegador], timeout=30)
        return sorted({l.split()[0] for l in out.splitlines() if "not found" in l})

    def pacotes_das_libs(self, libs):
        g = self.sis["gerenciador"]
        pk, desconhecidas = [], []
        for lib in libs:
            m = LIBS_CHROME.get(lib)
            if not m:
                desconhecidas.append(lib)
                continue
            if g == "apt":
                escolhido = next((c for c in m[0] if rodar(["apt-cache", "show", c], timeout=30)[0] == 0), m[0][-1])
                pk.append(escolhido)
            elif g == "dnf":
                pk.append(m[1])
        return sorted(set(pk)), desconhecidas

    def venv_python(self):
        return self.amb / "venv" / ("Scripts/python.exe" if WIN else "bin/python")

    def conf_whisper(self):
        py = self.venv_python()
        if not py.exists():
            return None
        rc, out = rodar([str(py), "-c", "import faster_whisper, ctranslate2, av; print(faster_whisper.__version__, ctranslate2.__version__, av.__version__)"], timeout=120)
        if rc != 0:
            return {"ok": False, "caminho": str(py)}
        fw, ct, av = out.strip().splitlines()[-1].split()
        return {"ok": True, "caminho": str(py), "faster_whisper": fw, "ctranslate2": ct, "av": av}

    def conf_tesseract(self):
        t = self.which("tesseract")
        if not t:
            return None
        rc, out = rodar([t, "--list-langs"], timeout=30)
        return {"caminho": t, "portugues": "por" in out.split()}

    # ---------- tabela
    def linha(self, item, estado, detalhe):
        self.linhas.append((item, estado, detalhe))

    def imprimir_tabela(self, titulo):
        print(f"\n{titulo}")
        print(f"  {'item':<28} {'estado':<11} detalhe")
        for item, estado, det in self.linhas:
            print(f"  {item:<28} {estado:<11} {det}")
        self.linhas = []

    # ---------- conferência inicial
    def conferencia_inicial(self):
        s = self.sis
        print("Sistema")
        print(f"  {s['versao_so']} ({s['so']} {s['arch']}), python {s['python']}")
        print(f"  gerenciador de pacotes: {s['gerenciador']}; privilégio: {s['privilegio']}")
        print(f"  rede: " + ", ".join(f"{h} {'ok' if v else 'SEM ACESSO'}" for h, v in s["rede"].items()))
        print(f"  disco livre: {s['disco_livre_gb']} GB; pasta: {self.pasta}")
        hf = self.perfil == "hyperframes"
        node = self.conf_node() if hf else None
        if hf:
            self.linha("node 22 ou mais", "ok" if node and node["ok"] else "instalando",
                       f"v{node['versao']} ({node['origem']})" if node and node["ok"] else (f"v{node['versao']} é antiga; baixo o node {VERSOES['node_local']} na pasta" if node else f"não achei; baixo o node {VERSOES['node_local']} na pasta"))
        for nome in ("ffmpeg", "ffprobe"):
            d = self.conf_ff(nome)
            if d:
                self.linha(nome, "ok", f"{d['versao']} ({d['origem']})")
            elif self.args.ffmpeg_sistema:
                self.linha(nome, "instalando" if s["pode_privilegio"] else "FALTA", "pacote de sistema (pedido com --ffmpeg-sistema)")
            else:
                self.linha(nome, "instalando", f"binário estático {VERSOES['ffmpeg_estatico']} em .ambiente/bin (sem privilégio)")
        if hf:
            for p in ("hyperframes", "gsap"):
                v = self.conf_pacote_npm(p)
                self.linha(p, "ok" if v == VERSOES[p] else "instalando",
                           f"v{v} na pasta" if v == VERSOES[p] else (f"v{v} na pasta; troco pela {VERSOES[p]}" if v else f"npm install {p}@{VERSOES[p]} na pasta"))
            nav = self.conf_navegador(node["caminho"]) if node and node["ok"] else None
            if nav and nav["headless"]:
                falt = self.libs_faltando(nav["caminho"])
                self.linha("Chrome do render", "ok", nav["caminho"])
                if s["so"] == "linux":
                    self.linha("bibliotecas do Chrome", "ok" if not falt else ("instalando" if s["pode_privilegio"] else "FALTA"),
                               "completas" if not falt else f"faltam {len(falt)}: {' '.join(falt[:6])}")
            else:
                self.linha("Chrome do render", "instalando", "hyperframes browser ensure (Chrome headless da versão fixada)")
                if s["so"] == "linux":
                    self.linha("bibliotecas do Chrome", "depois", "confiro depois do download do Chrome")
        pyv = sys.version_info[:2]
        self.linha("python 3.10 ou mais", "ok" if pyv >= VERSOES["python_minimo"] else "FALTA", f"{platform.python_version()} ({sys.executable})")
        w = self.conf_whisper()
        self.linha("faster-whisper (venv)", "ok" if w and w["ok"] else "instalando",
                   f"v{w['faster_whisper']} em .ambiente/venv" if w and w["ok"] else "venv em .ambiente/venv com faster-whisper 1.2.1")
        if hf:
            t = self.conf_tesseract()
            if t and t["portugues"]:
                self.linha("tesseract (opcional)", "ok", "com português")
            else:
                self.linha("tesseract (opcional)", "instalando" if s["pode_privilegio"] else "aviso",
                           ("sem o idioma português" if t else "ausente: a busca de prints fica por nome e data") + ("" if s["pode_privilegio"] else "; o dono pode instalar depois"))
        self.imprimir_tabela("Conferência inicial (ok = pronto, instalando = faço agora, FALTA = só o dono resolve, aviso = opcional)")

    # ---------- instalação, na ordem certa
    def garantir_pasta(self):
        if self.simular:
            if not self.pasta.exists():
                self.planos.append(("criar a pasta de trabalho", str(self.pasta)))
            return
        self.pasta.mkdir(parents=True, exist_ok=True)
        self.amb.mkdir(exist_ok=True)

    def instalar_node(self):
        node = self.conf_node()
        if node and node["ok"]:
            self.info["node"] = node
            self.path_extra.insert(0, Path(node["caminho"]).parent)
            return node
        if not self.precisa_rede("nodejs.org", "o node"):
            return None
        s = self.sis
        v = VERSOES["node_local"]
        plat = {"linux": "linux", "mac": "darwin", "windows": "win"}.get(s["so"])
        ext = "zip" if s["so"] == "windows" else ("tar.gz" if s["so"] == "mac" else "tar.xz")
        if not plat or s["arch"] not in ("x64", "arm64"):
            self.dono.append((f"node {VERSOES['node_minimo']}+ para {s['so']} {s['arch']}", "instale o node 22 LTS por https://nodejs.org e rode o instalador de novo"))
            return None
        nome = f"node-v{v}-{plat}-{s['arch']}"
        url = URL_NODE.format(v=v) + f"{nome}.{ext}"

        def baixar_node():
            dl = self.amb / "downloads"
            arq = dl / f"{nome}.{ext}"
            baixar(url, arq, timeout=120)
            somas = urllib.request.urlopen(URL_NODE.format(v=v) + "SHASUMS256.txt", timeout=30).read().decode()
            esperado = next((l.split()[0] for l in somas.splitlines() if l.endswith(f"{nome}.{ext}")), None)
            if not esperado or sha256(arq) != esperado:
                raise Saida(4, f"o download do node não confere com o SHASUMS256 oficial ({url})")
            alvo, tmp = self.amb / "node", self.amb / "node.extraindo"
            shutil.rmtree(tmp, ignore_errors=True)
            if ext == "zip":
                with zipfile.ZipFile(arq) as z:
                    z.extractall(tmp)
            else:
                with tarfile.open(arq) as t:
                    if hasattr(tarfile, "data_filter"):
                        t.extractall(tmp, filter="data")
                    else:
                        t.extractall(tmp)
            shutil.rmtree(alvo, ignore_errors=True)
            (tmp / nome).replace(alvo)
            shutil.rmtree(tmp, ignore_errors=True)
            arq.unlink()
            return round(os.path.getsize(alvo / ("node.exe" if WIN else "bin/node")) / 1e6, 1)

        self.passo_python(f"node {v} oficial em .ambiente/node (confere o SHA-256)", baixar_node,
                          f"baixar {url} e conferir com {URL_NODE.format(v=v)}SHASUMS256.txt; extrair em {self.amb / 'node'}")
        if self.simular:
            return {"caminho": str(self.amb / "node" / ("node.exe" if WIN else "bin/node")), "versao": v, "ok": True, "origem": "local"}
        node = self.conf_node()
        if not node or not node["ok"]:
            raise Saida(4, "baixei o node mas ele não roda nesta máquina")
        self.info["node"] = node
        self.path_extra.insert(0, Path(node["caminho"]).parent)
        return node

    def instalar_ff(self):
        s = self.sis
        for nome in ("ffmpeg", "ffprobe"):
            d = self.conf_ff(nome)
            if d:
                self.info[nome] = d
                continue
            if self.args.ffmpeg_sistema:
                # ffmpeg e ffprobe vêm no mesmo pacote: um passo só para os dois.
                if not getattr(self, "_ff_sistema_pedido", False):
                    self._ff_sistema_pedido = True
                    self.privilegiado("ffmpeg e ffprobe pelo gerenciador do sistema", comando_sistema(s, "ffmpeg"), "ffmpeg-sistema")
                if not self.simular:
                    self.info[nome] = self.conf_ff(nome)
                continue
            plat = {"linux": "linux", "mac": "darwin", "windows": "win32"}.get(s["so"])
            disponivel = plat and (s["arch"] in ("x64", "arm64", "ia32", "arm") if plat == "linux" else s["arch"] in (("x64", "arm64") if plat == "darwin" else ("x64",)))
            if not disponivel:
                self.privilegiado(f"{nome} (sem binário estático para {s['so']} {s['arch']})", comando_sistema(s, "ffmpeg"), "ffmpeg-sistema")
                continue
            if not self.precisa_rede("github.com", nome):
                continue
            arq = f"{nome}-{plat}-{s['arch']}"
            url = URL_FF.format(tag=VERSOES["ffmpeg_estatico"], arq=arq + ".gz")
            destino = self.amb / "bin" / f"{nome}{EXE}"

            def baixar_ff(url=url, destino=destino, arq=arq, nome=nome):
                gz = self.amb / "downloads" / (arq + ".gz")
                baixar(url, gz, timeout=300)
                destino.parent.mkdir(parents=True, exist_ok=True)
                tmp = destino.with_name(destino.name + ".novo")
                with gzip.open(gz, "rb") as fi, open(tmp, "wb") as fo:
                    shutil.copyfileobj(fi, fo)
                tmp.chmod(tmp.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
                tmp.replace(destino)
                gz.unlink()
                lic = self.amb / "bin" / "LICENCA-ffmpeg.txt"
                if not lic.exists():
                    try:
                        baixar(URL_FF.format(tag=VERSOES["ffmpeg_estatico"], arq=f"{plat}-{s['arch']}.LICENSE"), lic, timeout=60)
                    except Exception:
                        pass
                if rodar([str(destino), "-hide_banner", "-version"], timeout=30)[0] != 0:
                    raise Saida(4, f"o {nome} estático baixado não roda nesta máquina ({destino})")

            self.passo_python(f"{nome} estático {VERSOES['ffmpeg_estatico']} em .ambiente/bin (mesmo binário do pacote npm ffmpeg-static)", baixar_ff,
                              f"baixar {url}, descompactar em {destino} e conferir libx264 e aac")
            if not self.simular:
                d = self.conf_ff(nome)
                if not d:
                    raise Saida(4, f"o {nome} estático foi baixado mas reprovou na conferência (precisa de libx264 e aac)")
                self.info[nome] = d
        for nome in ("ffmpeg", "ffprobe"):
            d = self.info.get(nome)
            if d and d["origem"] == "local" and Path(d["caminho"]).parent not in self.path_extra:
                self.path_extra.insert(0, Path(d["caminho"]).parent)

    def instalar_npm(self, node):
        if not node:
            return
        faltam = [f"{p}@{VERSOES[p]}" for p in ("hyperframes", "gsap") if self.conf_pacote_npm(p) != VERSOES[p]]
        if faltam:
            if not self.precisa_rede("registry.npmjs.org", "o HyperFrames e o GSAP"):
                return
            pj = self.pasta / "package.json"
            if not pj.exists():
                # Sem package.json, o npm sobe de pasta em pasta e pode instalar no lugar errado.
                if self.simular:
                    self.planos.append(("criar package.json mínimo na pasta (o npm instala aqui e não numa pasta acima)", str(pj)))
                else:
                    pj.write_text(json.dumps({"name": "edicao-video", "private": True, "description": "pasta de trabalho das skills de edição"}, indent=2) + "\n", encoding="utf-8")
            npm = self.npm_cmd(node["caminho"]) if not self.simular or Path(node["caminho"]).exists() else [str(Path(node["caminho"]).parent / "npm")]
            if not npm:
                raise Saida(4, "achei o node mas não o npm; reinstale o node completo (vem com npm)")
            self.executar(f"npm install {' '.join(faltam)} na pasta", npm + ["install", "--save-exact", "--no-audit", "--no-fund", "--loglevel=error"] + faltam,
                          "npm-install", cwd=self.pasta if self.pasta.exists() else None)
        if not self.simular:
            for p in ("hyperframes", "gsap"):
                v = self.conf_pacote_npm(p)
                if v != VERSOES[p]:
                    raise Saida(4, f"depois do npm install, {p} está em {v}, esperado {VERSOES[p]}")
                self.info[p] = {"versao": v, "caminho": str(self.pasta / "node_modules" / p)}
            self.info["gsap"]["arquivo"] = str(self.pasta / "node_modules/gsap/dist/gsap.min.js")
            self.info["hyperframes"]["bin"] = str(self.hf_bin())

    def instalar_navegador(self, node):
        if not node:
            return
        nav = None if self.simular else self.conf_navegador(node["caminho"])
        if self.simular and self.hf_bin().exists():
            nav = self.conf_navegador(node["caminho"])
        if not nav or not nav["headless"]:
            if not self.precisa_rede("storage.googleapis.com", "o Chrome do render"):
                return
            self.executar("Chrome headless do HyperFrames (hyperframes browser ensure)", [node["caminho"], str(self.hf_bin()), "browser", "ensure"],
                          "browser-ensure", cwd=self.pasta if self.pasta.exists() else None, timeout=1800)
            if self.simular:
                if self.sis["so"] == "linux":
                    self.planos.append(("conferir as bibliotecas do Chrome com ldd", "ldd <chrome-headless-shell>; se faltar alguma, instalar pelo gerenciador (privilégio)"))
                return
            nav = self.conf_navegador(node["caminho"])
            if not nav:
                raise Saida(4, "o browser ensure terminou mas o HyperFrames não acha o Chrome (veja .ambiente/logs/browser-ensure.log)")
        self.info["navegador"] = nav
        falt = self.libs_faltando(nav["caminho"])
        if falt:
            pk, desconhecidas = self.pacotes_das_libs(falt)
            cmd = comando_sistema(self.sis, "libs", pk) if pk else None
            motivo = f"bibliotecas de sistema do Chrome: {' '.join(falt)}" + (f" (sem pacote mapeado: {' '.join(desconhecidas)})" if desconhecidas else "")
            if self.privilegiado(motivo, cmd, "libs-chrome") and not self.simular:
                falt = self.libs_faltando(nav["caminho"])
                if falt:
                    raise Saida(4, f"instalei os pacotes mas ainda faltam: {' '.join(falt)}")
        self.info["navegador"]["libs_faltando"] = falt

    def instalar_whisper(self):
        if sys.version_info[:2] < VERSOES["python_minimo"]:
            cmd = comando_sistema(self.sis, "venv", ["python3.12"] if self.sis["gerenciador"] in ("apt", "dnf") else None)
            self.dono.append((f"python {platform.python_version()} é antigo para o faster-whisper (precisa 3.10 ou mais)",
                              (comando_dono(cmd) + " e rode o instalador com esse python") if cmd else "instale o python 3.12 por https://www.python.org e rode o instalador com ele"))
            return
        w = self.conf_whisper()
        if w and w["ok"]:
            self.info["whisper"] = w
            return
        py = self.venv_python()
        venv = self.amb / "venv"
        if not py.exists():
            if self.simular:
                self.planos.append(("criar o venv em .ambiente/venv", mostra_cmd([sys.executable, "-m", "venv", str(venv)])))
            else:
                rc, out = rodar([sys.executable, "-m", "venv", str(venv)], log=self.logs / "venv.log", timeout=300)
                if rc != 0:
                    # python sem ensurepip (Debian e Ubuntu sem python3-venv): venv sem pip e pip pelo get-pip oficial
                    shutil.rmtree(venv, ignore_errors=True)
                    rc, out = rodar([sys.executable, "-m", "venv", "--without-pip", str(venv)], log=self.logs / "venv.log", timeout=300)
                    ok = rc == 0 and self.sis["rede"].get("pypi.org")
                    if ok:
                        try:
                            baixar(URL_GETPIP, self.amb / "downloads" / "get-pip.py", timeout=120)
                            ok = rodar([str(py), str(self.amb / "downloads" / "get-pip.py"), "-q"], log=self.logs / "venv.log", timeout=600)[0] == 0
                        except Exception:
                            ok = False
                    if not ok:
                        shutil.rmtree(venv, ignore_errors=True)
                        v = f"python{sys.version_info[0]}.{sys.version_info[1]}-venv" if self.sis["gerenciador"] == "apt" else None
                        self.privilegiado("o python desta máquina não cria venv", comando_sistema(self.sis, "venv", [v] if v else None), "venv-sistema")
                        if not self.simular and rodar([sys.executable, "-m", "venv", str(venv)], log=self.logs / "venv.log")[0] != 0:
                            return
                    else:
                        self.feitos.append(("venv sem ensurepip, pip pelo get-pip oficial", 0))
        if not self.precisa_rede("pypi.org", "o faster-whisper"):
            return
        pip = [str(py), "-m", "pip", "install", "-q"]
        if self.simular:
            self.planos.append(("faster-whisper e dependências fixadas no venv", mostra_cmd(pip + VERSOES["pip_fixado"])))
            self.planos.append(("se a combinação fixada não tiver pacote para este python", mostra_cmd(pip + VERSOES["pip_reserva"])))
            return
        try:
            self.executar("faster-whisper 1.2.1 com ctranslate2 4.7.2 e av 17.0.1 (combinação provada)", pip + VERSOES["pip_fixado"], "pip")
        except Saida:
            print(f"    a combinação fixada não instalou neste python; tentando a de reserva ({' '.join(VERSOES['pip_reserva'])})")
            self.executar("faster-whisper 1.2.1 com av abaixo da 19 (reserva)", pip + VERSOES["pip_reserva"], "pip")
        w = self.conf_whisper()
        if not w or not w["ok"]:
            raise Saida(4, "o faster-whisper instalou mas não importa no venv (veja .ambiente/logs/pip.log)")
        self.info["whisper"] = w

    def instalar_tesseract(self):
        t = self.conf_tesseract()
        if t and t["portugues"]:
            self.info["tesseract"] = t
            return
        cmd = comando_sistema(self.sis, "tesseract")
        if self.sis["pode_privilegio"] and cmd:
            try:
                self.executar("tesseract com português (opcional)", cmd, "tesseract")
            except Saida as e:
                print(f"    aviso: o tesseract é opcional e não instalou ({e.msg.splitlines()[0]})")
            self.info["tesseract"] = None if self.simular else self.conf_tesseract()
        else:
            self.info["tesseract"] = t
            self.info["tesseract_comando"] = comando_dono(cmd) if cmd else "instale o tesseract com o idioma português"

    # ---------- ambiente.json e ativadores
    def gravar(self):
        env = {"HYPERFRAMES_NO_TELEMETRY": "1", "HYPERFRAMES_NO_UPDATE_CHECK": "1"}
        if self.perfil == "hyperframes":
            env["EDICAO_FERRAMENTAS"] = str(self.pasta)
        if self.info.get("whisper"):
            env["WHISPER_PYTHON"] = self.info["whisper"]["caminho"]
        for nome, var in (("ffmpeg", "HYPERFRAMES_FFMPEG_PATH"), ("ffprobe", "HYPERFRAMES_FFPROBE_PATH")):
            if self.info.get(nome) and self.info[nome]["origem"] == "local":
                env[var] = self.info[nome]["caminho"]
        prefixo = [str(p) for p in self.path_extra if str(p).startswith(str(self.amb))]
        dados = {
            "perfil": self.perfil, "pasta": str(self.pasta),
            "sistema": {k: self.sis[k] for k in ("so", "arch", "gerenciador", "privilegio")},
            "versoes_fixadas": {k: VERSOES[k] for k in ("hyperframes", "gsap", "node_local", "ffmpeg_estatico")} if self.perfil == "hyperframes" else {"ffmpeg_estatico": VERSOES["ffmpeg_estatico"]},
            "node": self.info.get("node"), "ffmpeg": self.info.get("ffmpeg"), "ffprobe": self.info.get("ffprobe"),
            "hyperframes": self.info.get("hyperframes"), "gsap": self.info.get("gsap"), "navegador": self.info.get("navegador"),
            "whisper": self.info.get("whisper"), "tesseract": self.info.get("tesseract"),
            "path_prefixo": prefixo, "env": env,
            "ativar": {"linux_mac": f'. "{self.amb / "ativar.sh"}"', "windows_cmd": f'call "{self.amb / "ativar.bat"}"'},
        }
        if self.perfil == "ffmpeg":
            for k in ("node", "hyperframes", "gsap", "navegador", "tesseract"):
                dados.pop(k)
        sh = "# gerado pelo instalar_ambiente.py: carregue antes de editar\n"
        if prefixo:
            sh += f'export PATH="{":".join(prefixo)}:$PATH"\n'
        sh += "".join(f'export {k}="{v}"\n' for k, v in env.items())
        bat = "@echo off\r\nrem gerado pelo instalar_ambiente.py: carregue antes de editar\r\n"
        if prefixo:
            bat += f'set "PATH={";".join(prefixo)};%PATH%"\r\n'
        bat += "".join(f'set "{k}={v}"\r\n' for k, v in env.items())
        mudou = False
        for arq, conteudo in ((self.pasta / "ambiente.json", json.dumps(dados, indent=2, ensure_ascii=False) + "\n"),
                              (self.amb / "ativar.sh", sh), (self.amb / "ativar.bat", bat)):
            novo = conteudo.encode("utf-8")
            if not arq.exists() or arq.read_bytes() != novo:
                arq.write_bytes(novo)
                mudou = True
        return dados, mudou

    # ---------- conferência final
    def conferencia_final(self, dados):
        reprova = []

        def item(nome, ok, det, obrig=True):
            self.linha(nome, "ok" if ok else ("FALTA" if obrig else "aviso"), det)
            if not ok and obrig:
                reprova.append(nome)

        if self.perfil == "hyperframes":
            n = dados.get("node")
            item("node 22 ou mais", bool(n and n["ok"]), f"v{n['versao']} ({n['origem']}) {n['caminho']}" if n else "ausente")
        for nome in ("ffmpeg", "ffprobe"):
            d = dados.get(nome)
            item(nome, bool(d), f"{d['versao']} ({d['origem']}) {d['caminho']}" if d else "ausente")
        if self.perfil == "hyperframes":
            for p in ("hyperframes", "gsap"):
                d = dados.get(p)
                item(p, bool(d and d["versao"] == VERSOES[p]), f"v{d['versao']} na pasta" if d else "ausente")
            nav = dados.get("navegador")
            item("Chrome do render", bool(nav and nav["headless"]), nav["caminho"] if nav else "ausente")
            if self.sis["so"] == "linux":
                item("bibliotecas do Chrome", bool(nav) and not nav.get("libs_faltando"), "completas" if nav and not nav.get("libs_faltando") else "faltam bibliotecas")
        w = dados.get("whisper")
        item("faster-whisper (venv)", bool(w and w["ok"]), f"v{w['faster_whisper']} (ctranslate2 {w['ctranslate2']}, av {w['av']}) {w['caminho']}" if w else "ausente")
        if self.perfil == "hyperframes":
            t = dados.get("tesseract")
            item("tesseract (opcional)", bool(t and t["portugues"]), "com português" if t and t["portugues"] else
                 f"sem OCR; para ter: {self.info.get('tesseract_comando', 'instale o tesseract com português')}", obrig=False)
        self.imprimir_tabela("Conferência final")
        return reprova

    def rodar(self):
        hf = self.perfil == "hyperframes"
        self.conferencia_inicial()
        if self.sis["disco_livre_gb"] < (1.5 if hf else 0.8):
            self.dono.append((f"pouco disco livre ({self.sis['disco_livre_gb']} GB)", f"libere pelo menos {'1,5' if hf else '0,8'} GB na partição da pasta {self.pasta}"))
            return self.fim()
        self.garantir_pasta()
        node = self.instalar_node() if hf else None
        self.instalar_ff()
        if hf:
            self.instalar_npm(node)
            self.instalar_navegador(node)
        self.instalar_whisper()
        if hf:
            self.instalar_tesseract()
        return self.fim()

    def fim(self):
        if self.simular:
            print("\nModo simular: nada foi executado. Isto é o que eu faria, nesta ordem:")
            for i, (d, c) in enumerate(self.planos, 1):
                print(f"  {i}. {d}\n     {c}")
            if not self.planos:
                print("  nada: o ambiente já está pronto.")
            return self.pedir_dono() if self.dono else 0
        if self.dono:
            # Grava o que deu para instalar e para no pedido ao dono.
            if self.pasta.exists():
                self.gravar()
            return self.pedir_dono()
        dados, mudou = self.gravar()
        reprova = self.conferencia_final(dados)
        print(f"\nambiente.json: {self.pasta / 'ambiente.json'} ({'gravado' if mudou else 'sem mudança'})")
        if self.feitos:
            print("Instalado agora: " + "; ".join(f"{d} ({s:.0f} s)" for d, s in self.feitos))
        else:
            print("Nada a instalar: o ambiente já estava pronto.")
        if dados["path_prefixo"]:
            print(f"Antes de editar, carregue o ambiente: {dados['ativar']['windows_cmd' if WIN else 'linux_mac']}")
        if reprova:
            print(f"\nA conferência final reprovou: {', '.join(reprova)}. Veja os logs em {self.logs}.")
            return 1
        print("\nAmbiente pronto. Próximo passo: a prova de render (prova_render.py).")
        return 0

    def pedir_dono(self):
        print("\nFalta algo que só o dono da máquina resolve. Diga ao dono, em uma frase, e espere ele rodar:")
        for motivo, cmd in self.dono:
            print(f"  motivo: {motivo}\n  comando: {cmd}")
        print("Depois que o dono rodar, rode este instalador de novo.")
        return 3


def main():
    ap = ParserPt(description="Instala o ambiente das skills de edição de vídeo e grava ambiente.json na pasta.")
    ap.add_argument("--perfil", required=True, choices=["hyperframes", "ffmpeg"], help="hyperframes ou ffmpeg")
    ap.add_argument("--pasta", required=True, help="pasta de trabalho da edição")
    ap.add_argument("--simular", action="store_true", help="mostra tudo que faria, sem executar nada")
    ap.add_argument("--sem-privilegio", action="store_true", help="não usa sudo nem administrador, mesmo que exista")
    ap.add_argument("--ffmpeg-sistema", action="store_true", help="instala o ffmpeg pelo gerenciador do sistema em vez do binário estático")
    ap.add_argument("--so-ffmpeg-local", action="store_true", help=argparse.SUPPRESS)  # ignora o ffmpeg do PATH (teste)
    args = ap.parse_args()
    if args.ffmpeg_sistema and args.so_ffmpeg_local:
        ap.error("--ffmpeg-sistema e --so-ffmpeg-local não combinam")
    t = time.time()
    try:
        codigo = Instalador(args).rodar()
    except Saida as e:
        print(f"\nERRO: {e.msg}", file=sys.stderr)
        codigo = e.codigo
    except KeyboardInterrupt:
        print("\ninterrompido; rode de novo que ele continua de onde parou", file=sys.stderr)
        codigo = 4
    print(f"(saída {codigo}, {time.time() - t:.0f} s)")
    sys.exit(codigo)


if __name__ == "__main__":
    main()
