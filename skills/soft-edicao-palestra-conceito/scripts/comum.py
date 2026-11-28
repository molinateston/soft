"""Funcoes comuns: acha a skill, le marca.json e ajustes.json da pasta de trabalho, converte cores.
Nenhum caminho fixo: tudo e relativo a pasta da skill ou a pasta de trabalho passada na linha de comando."""
import json, os, sys, subprocess

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(SCRIPTS)
FPS = 30
W, H = 1080, 1920
WV, HV = 1080, 608            # faixa do palestrante (16:9)
YV = (H - HV) // 2            # 656: fim da tarja de cima
YB = YV + HV                  # 1264: inicio da tarja de baixo
HB = H - YB                   # 656: altura da tarja de baixo
CAP_Y = YV + HV - 92          # centro da legenda, fixo, na parte de baixo do video


def trab_arg(i=1):
    if len(sys.argv) <= i:
        sys.exit(f'uso: python3 {os.path.basename(sys.argv[0])} PASTA_DE_TRABALHO [...]')
    t = os.path.abspath(sys.argv[i])
    os.makedirs(t, exist_ok=True)
    return t


def marca(trab=None):
    p = os.path.join(trab, 'marca.json') if trab else ''
    if not (p and os.path.exists(p)):
        p = os.path.join(RAIZ, 'marca.json')
    return json.load(open(p))


def ajustes(trab):
    p = os.path.join(trab, 'ajustes.json')
    if not os.path.exists(p):
        sys.exit(f'falta {p} (copie exemplo/ajustes.json e preencha)')
    return json.load(open(p))


def fonte_arq(M, chave):
    f = M['fontes'][chave]
    return f if os.path.isabs(f) else os.path.join(RAIZ, f)


def rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def cor(M, chave):
    return rgb(M['cores'][chave])


def lj(trab, nome):
    return json.load(open(os.path.join(trab, nome)))


def gj(trab, nome, obj):
    json.dump(obj, open(os.path.join(trab, nome), 'w'), ensure_ascii=False, indent=1)


def duracao(arq):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                                          '-of', 'csv=p=0', arq]).decode())


def tamanho(arq):
    o = subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                                 'stream=width,height', '-of', 'csv=p=0', arq]).decode().strip()
    w, h = o.split(',')[:2]
    return int(w), int(h)


def palavras_bruto(trab):
    """palavras da transcricao do bruto em tempo ABSOLUTO da fonte: [{t0,t1,w}]"""
    T = lj(trab, 'transcricao.json')
    segs = T['segmentos'] if isinstance(T, dict) else T
    ws = [dict(t0=p['t0'], t1=p['t1'], w=p['w'].strip()) for s in segs for p in s['palavras']]
    return sorted(ws, key=lambda w: w['t0'])
