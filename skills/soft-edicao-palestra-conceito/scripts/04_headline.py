"""Etapa 4. Headline e sub da tarja de cima: confere qualidade e encaixe, gera topo-previa.png.
Le ajustes.json > headline {headline, sub, destaque[], size?, sub_size?, linhas?, sub_linhas?}
e TRAB/headlines.md (3 candidatas, uma marcada ESCOLHIDA, com o porque).
uso: python3 04_headline.py TRAB
criterio de pronto (PRONTO, exit 0): headline em ate 2 linhas sem palavra sozinha na 2a linha, cada linha
<= largura_max_linha px, sub em ate 2 linhas, destaque existe na headline, sem travessao, headlines.md com
3 candidatas e ESCOLHIDA, sem travessao; lint_copy exit 0 se marca.lint_copy ou LINT_COPY apontar um linter."""
import os, re, subprocess, sys, tempfile
import comum as C
import tarjas

T = C.trab_arg()
M, A = C.marca(T), C.ajustes(T)
HL = A['headline']
img, lg = tarjas.topo(M, HL)
img.save(os.path.join(T, 'topo-previa.png'))
tz = M['tamanhos']
f = []
if len(lg['linhas']) > tz['headline_max_linhas']: f.append(f"headline em {len(lg['linhas'])} linhas (max {tz['headline_max_linhas']}): encurte ou baixe size")
if len(lg['linhas']) == 2 and len(lg['linhas'][1].split()) == 1: f.append(f"palavra sozinha na 2a linha: {lg['linhas'][1]!r}")
if len(lg['sub_linhas']) > tz['sub_max_linhas']: f.append(f"sub em {len(lg['sub_linhas'])} linhas (max {tz['sub_max_linhas']})")
for ln, w in zip(lg['linhas'] + lg['sub_linhas'], lg['larguras']):
    if w > tz['largura_max_linha']: f.append(f'linha {ln!r} com {w} px (max {tz["largura_max_linha"]})')
palav = {x.strip('.,?!') for x in HL['headline'].split()}
for d in HL.get('destaque', []):
    if d.strip('.,?!') not in palav: f.append(f'destaque {d!r} nao esta na headline')
for k in ('headline', 'sub'):
    if re.search('[—–]', HL[k]): f.append(f'travessao na {k}')
hm = os.path.join(T, 'headlines.md')
if not os.path.exists(hm): f.append('falta headlines.md com 3 candidatas')
else:
    t = open(hm).read()
    n = len(re.findall(r'(?im)^\s*(\d+[.)]|-)?\s*\**headline\**\s*:', t))
    if n < 3: f.append(f'headlines.md tem {n} candidatas (minimo 3, cada uma com "Headline:" e "Sub:")')
    if 'ESCOLHIDA' not in t: f.append('headlines.md sem a marca ESCOLHIDA')
lint = M.get('lint_copy') or os.environ.get('LINT_COPY')   # linter de copy do cliente, opcional
if lint:
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as tf:
        tf.write(HL['headline'] + '\n' + HL['sub'] + '\n')
    r = subprocess.run([sys.executable, lint, tf.name], capture_output=True, text=True)
    os.unlink(tf.name)
    print(r.stdout.strip())
    if r.returncode: f.append('lint_copy reprovou (veja acima)')
print('linhas:', lg['linhas'], '| sub:', lg['sub_linhas'], '| larguras px:', lg['larguras'], '| size', lg['size'], lg['sub_size'])
for x in f: print('FALHA', x)
print('PRONTO' if not f else 'NAO PRONTO', '-> topo-previa.png')
sys.exit(1 if f else 0)
