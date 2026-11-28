"""Etapa 9. Entrega: so roda com os dois gates sem falha. Monta TRAB/entrega/ com
  SLUG-master.mp4 (o final.mp4), SLUG-leve.mp4 (2 passes, 1050 kb/s, aac 96 kb/s, para WhatsApp e revisao),
  edit-manifest.json (cortes, velocidade, legenda, conceitos, gates), verbos-pedido.json (cada verbo do pedido com o
  numero medido antes e depois) e legenda-post.txt (CTA da marca: o video nao leva CTA queimado).
uso: python3 09_entrega.py TRAB [--prova]     (SLUG = ajustes.slug, padrao 'reel')
criterio de pronto: PRONTO, exit 0; a pasta entrega/ tem os 5 arquivos. Nada e enviado para fora da maquina."""
import os, shutil, subprocess, sys
import comum as C

T = C.trab_arg()
PROVA = '--prova' in sys.argv
M, A, E = C.marca(T), C.ajustes(T), C.lj(T, 'entrada.json')
CC, CO, RL = C.lj(T, 'cortes.json'), C.lj(T, 'conceitos.json'), C.lj(T, 'render-log.json')
GF, GV = C.lj(T, 'gate-fala.json'), C.lj(T, 'gate-visual.json')
f = [f'gate de fala: {x}' for x in GF['falhas']] + [f'gate visual: {x}' for x in GV['falhas']]
if RL.get('parcial') and not PROVA: f.append('final.mp4 e um render parcial (--ate): rode 06_compor.py sem --ate')
if f:
    for x in f: print('FALHA', x)
    print('NAO PRONTO: corrija e rode os gates de novo'); sys.exit(1)
S = A.get('slug', 'reel') + ('-prova' if PROVA else '')
OUT = os.path.join(T, 'entrega'); os.makedirs(OUT, exist_ok=True)
FIN, MAS, LEV = os.path.join(T, 'final.mp4'), os.path.join(OUT, f'{S}-master.mp4'), os.path.join(OUT, f'{S}-leve.mp4')
shutil.copy2(FIN, MAS)
pl = os.path.join(T, 'ff2pass')
for p, extra in ((1, ['-an', '-f', 'mp4', os.devnull]), (2, ['-c:a', 'aac', '-b:a', '96k', '-movflags', '+faststart', LEV])):
    subprocess.run(['nice', '-n', '15', 'ffmpeg', '-v', 'error', '-y', '-i', FIN, '-c:v', 'libx264', '-preset', 'slow', '-b:v', '1050k',
                    '-pass', str(p), '-passlogfile', pl, '-pix_fmt', 'yuv420p'] + extra, check=True)
for x in os.listdir(T):
    if x.startswith('ff2pass'): os.remove(os.path.join(T, x))
dur, fonte = GV['dur'], sum(b - a for a, b in CC['keep'])
corpo = [b for b in CC['blocos'] if not b['cold']]
bruto = sum(b['fim'] - b['ini'] for b in corpo)
pal = C.lj(T, 'palavras-saida.json')
v = lambda verbo, est, m: dict(verbo=verbo, estado=est, motivo_medido=m)
br = lambda x: f'{x:.2f}'.replace('.', ',')
verbos = [
    v('cortar', 'feito', f"fonte: {br(bruto)} s em {len(corpo)} bloco(s) · final: {len(CC['keep'])} pecas somando {br(fonte)} s de fonte · diferenca: {br(bruto - fonte + (CC['cold_open'][1] - CC['cold_open'][0] if CC.get('cold_open') else 0))} s de pausa removidos"),
    v('acelerar', 'feito', f"fonte: 1,00x, {br(fonte)} s · final: {br(CC['velocidade'])}x (atempo, sem mudar o tom), {br(dur)} s · diferenca: {br(fonte - dur)} s a menos"),
    v('verticalizar', 'feito', f"fonte: {E['largura']}x{E['altura']} · final: {C.W}x{C.H}, video {C.WV}x{C.HV} entre a tarja da headline e a do desenho · diferenca: quadro vertical"),
    v('legendar', 'feito', f"fonte: 0 palavras queimadas · final: {len(pal)} palavras, 1 por vez, fixa em y {RL['cap_y']} · diferenca: +{len(pal)} palavras, cobertura de fala {GF['cobertura']:.1%}"),
    v('titular', 'feito', f"fonte: sem headline · final: headline '{CO['headline']['headline']}' e sub fixas do quadro 0 ao fim · diferenca: +1 headline, +1 sub"),
    v('desenhar', 'feito', f"fonte: 0 desenhos · final: {len(CO['conceitos'])} conceitos em line drawing na tarja de baixo · diferenca: +{len(CO['conceitos'])} desenhos"),
    v('ganchar', 'feito' if CC.get('cold_open') else 'nao_aplicavel',
      f"final: cold open de {br(CC['cold_saida'])} s ({br(CC['cold_open'][0])} a {br(CC['cold_open'][1])} s da fonte) antes do inicio" if CC.get('cold_open') else 'sem cold open: o trecho ja abre forte'),
    v('musicar', 'nao_aplicavel', 'fonte: sem musica · final: sem musica · diferenca: nenhuma, a marca proibe musica' if M.get('musica') is False else 'marca permite musica; esta skill nao poe'),
]
C.gj(OUT, 'verbos-pedido.json', verbos)
C.gj(OUT, 'edit-manifest.json', dict(
    layout_mode='top-fixed', caption_mode='word', caption_y=RL['cap_y'], speech_speed=CC['velocidade'],
    fonte=os.path.basename(E['fonte']), blocos=[[b['ini'], b['fim']] for b in corpo], cold_open=CC.get('cold_open'),
    cut_map=CC['cut_map'], timeline_duration=dur, headline=CO['headline'],
    conceitos=[dict(id=c['id'], t=c['t'], fala=c.get('fala'), mostra=c.get('mostra')) for c in CO['conceitos']],
    render_order=['tarja_topo_headline', 'video', 'tarja_baixo_desenho', 'legenda'], music='nenhuma' if M.get('musica') is False else 'permitida',
    gates=dict(fala=dict(cobertura=GF['cobertura'], avisos=GF['avisos']), visual=dict(avisos=GV['avisos'])),
    arquivos=[os.path.basename(MAS), os.path.basename(LEV)], prova=PROVA))
open(os.path.join(OUT, 'legenda-post.txt'), 'w').write((M.get('cta') or {}).get('texto', '') + '\n')
for x in sorted(os.listdir(OUT)): print(f'{os.path.getsize(os.path.join(OUT, x)) / 1e6:8.2f} MB  {x}')
print('PRONTO ->', OUT)
