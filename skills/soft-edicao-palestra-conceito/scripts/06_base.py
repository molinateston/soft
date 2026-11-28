"""Etapa 6a. Base: corta as pecas direto da fonte, acelera (velocidade da marca) e junta.
uso: python3 06_base.py TRAB
saidas: base.mkv (video no tamanho da fonte, 30 fps, sem audio), audio.wav (48 kHz, loudnorm -14 LUFS).
Cada bloco tem cache (bN.mkv + bN.assin): so re-renderiza o bloco que mudou.
criterio de pronto: imprime PRONTO; duracao de base.mkv = dur_saida de cortes.json (+-1 quadro)."""
import os, subprocess, sys
import comum as C

T = C.trab_arg()
E, CC = C.lj(T, 'entrada.json'), C.lj(T, 'cortes.json')
SPD, FPS = CC['velocidade'], C.FPS
NICE = ['nice', '-n', '10']
lst = []
for bi, b in enumerate(CC['blocos']):
    s0, e0 = b['keep'][0][0], b['keep'][-1][1]
    fc, n = [], len(b['keep'])
    for i, (a, c) in enumerate(b['keep']):
        a0, d = a - s0, c - a
        fc.append(f'[0:v]trim={a0:.4f}:{a0 + d:.4f},setpts=PTS-STARTPTS[v{i}]')
        fc.append(f'[0:a]atrim={a0:.4f}:{a0 + d:.4f},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st={d - 0.03:.4f}:d=0.03[a{i}]')
    fc.append(''.join(f'[v{i}][a{i}]' for i in range(n)) + f'concat=n={n}:v=1:a=1[vc][ac]')
    fc.append(f'[vc]setpts=PTS/{SPD},fps={FPS},trim=end_frame={b["nq"]},setsar=1[vo]')
    fc.append(f'[ac]atempo={SPD},aresample=48000,apad,atrim=end_sample={round(b["nq"] / FPS * 48000)}[ao]')
    out = os.path.join(T, f'b{bi}.mkv'); ass = os.path.join(T, f'b{bi}.assin')
    assin = ';\n'.join(fc) + f'\n#{E["fonte"]} {s0:.4f} {e0:.4f}'
    lst.append(f"file '{out}'")
    if os.path.exists(out) and os.path.exists(ass) and open(ass).read() == assin:
        print('bloco', bi, 'igual, mantido'); continue
    open(os.path.join(T, f'fc{bi}.txt'), 'w').write(';\n'.join(fc))
    subprocess.run(NICE + ['ffmpeg', '-v', 'error', '-y', '-ss', f'{s0:.4f}', '-t', f'{e0 - s0 + 0.5:.3f}', '-i', E['fonte'],
                           '-filter_complex_script', os.path.join(T, f'fc{bi}.txt'), '-map', '[vo]', '-map', '[ao]',
                           '-c:v', 'libx264', '-crf', '10', '-preset', 'fast', '-c:a', 'pcm_s16le', out], check=True)
    open(ass, 'w').write(assin)
    print('bloco', bi, 'ok', flush=True)
open(os.path.join(T, 'blocos.txt'), 'w').write('\n'.join(lst) + '\n')
subprocess.run(NICE + ['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', os.path.join(T, 'blocos.txt'),
                       '-map', '0:v', '-c:v', 'copy', os.path.join(T, 'base.mkv'),
                       '-map', '0:a', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000', '-c:a', 'pcm_s16le', os.path.join(T, 'audio.wav')], check=True)
d = C.duracao(os.path.join(T, 'base.mkv'))
ok = abs(d - CC['dur_saida']) <= 1.5 / FPS
print(f'base {d:.3f} s (esperado {CC["dur_saida"]:.3f})', 'PRONTO' if ok else 'NAO PRONTO')
sys.exit(0 if ok else 1)
