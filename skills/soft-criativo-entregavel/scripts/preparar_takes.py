"""Recorta os takes de video do entregavel (definidos em oferta.json -> "takes") em arquivos .npy para o render ler quadro a quadro.
    python preparar_takes.py <pasta_do_kit_da_oferta> [nome1 nome2 ...]
oferta.json:  "takes": {"tablet_capa": {"arquivo": "Assets/VIDEOS OUTROS/TABLET 01.MOV", "inicio": 0.2, "dur": 5.0}, ...}
    arquivo: relativo a pasta raiz da oferta;  inicio/dur em segundos do video original (escolher olhando uma folha de quadros).
Cada take vira <kit>/takes/<nome>.npy em 720x1280 a 30 qps (~83 MB por segundo): manter os takes curtos (3 a 7 s).
So refaz os que ainda nao existem.
"""
import sys, os, json, subprocess
import numpy as np
W, H = 720, 1280
if __name__ == '__main__':
    kit = os.path.abspath(sys.argv[1]); OF = json.load(open(os.path.join(kit, 'oferta.json'), encoding='utf-8')); raiz = OF.get('raiz') or os.path.dirname(kit)
    os.makedirs(os.path.join(kit, 'takes'), exist_ok=True)
    for name, tk in OF.get('takes', {}).items():
        if sys.argv[2:] and name not in sys.argv[2:]: continue
        out = os.path.join(kit, 'takes', name + '.npy')
        if os.path.exists(out): print(name, 'ja existe'); continue
        src = tk['arquivo'] if os.path.isabs(tk['arquivo']) else os.path.join(raiz, tk['arquivo']); n = int(round(tk['dur'] * 30))
        b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(tk['inicio']), '-i', src, '-frames:v', str(n), '-vf',
                            f'fps=30,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}', '-an', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
        a = np.frombuffer(b, np.uint8).reshape(-1, H, W, 3); np.save(out, a); print(name, a.shape, '%.0f MB' % (a.nbytes / 1e6), flush=True)
