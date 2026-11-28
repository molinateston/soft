"""Etapa 8. Mosaico para olhar o video inteiro de uma vez: 24 quadros (grade 8 x 3) + quadros 0, 1, 3 e 5 s em tamanho cheio.
uso: python3 08_mosaico.py TRAB     saidas: mosaico.jpg, quadro-0s.jpg, quadro-1s.jpg, quadro-3s.jpg, quadro-5s.jpg
criterio de pronto: os arquivos existem E quem edita olhou e confirmou, quadro a quadro:
headline legivel e inteira; rosto do palestrante inteiro na faixa (testa e queixo); legenda sem cobrir a boca;
desenho bate com a fala do momento; nenhum quadro preto, verde ou com slide errado."""
import os, subprocess, sys
from PIL import Image
import comum as C

T = C.trab_arg()
FIN = os.path.join(T, 'final.mp4')
dur = C.duracao(FIN)
CW, CH, COLS, ROWS = 270, 480, 8, 3
mos = Image.new('RGB', (CW * COLS, CH * ROWS), 'white')
for k in range(COLS * ROWS):
    t = (k + 0.5) * dur / (COLS * ROWS)
    raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', FIN, '-frames:v', '1', '-vf', f'scale={CW}:{CH}',
                                   '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
    if len(raw) == CW * CH * 3: mos.paste(Image.frombytes('RGB', (CW, CH), raw), ((k % COLS) * CW, (k // COLS) * CH))
mos.save(os.path.join(T, 'mosaico.jpg'), quality=85)
for s in (0, 1, 3, 5):
    if s < dur:
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(s), '-i', FIN, '-frames:v', '1', '-q:v', '3', os.path.join(T, f'quadro-{s}s.jpg')], check=True)
print('mosaico.jpg + quadro-{0,1,3,5}s.jpg em', T)
print('PRONTO para olhar: abra mosaico.jpg e quadro-0s.jpg e confira a lista do cabecalho deste script')
