# Ganho uniforme pequeno só no áudio (vídeo copiado, cor intacta), para abrir espaço ao som do GIF com true peak <= -1 dBTP.
# Uso do EP4: o Gancho B, de áudio original alto, levou -1 dB antes do GIF. Regra: no máximo -2 dB; acima disso, revise o mix.
# Uso: python3 ganho_uniforme.py entrada.mp4 saida.mp4 --db -1
import json, re, subprocess, argparse, sys
ap = argparse.ArgumentParser(description='ganho uniforme no áudio, vídeo copiado'); ap.add_argument('entrada'); ap.add_argument('saida')
ap.add_argument('--db', type=float, required=True, help='ganho em dB (negativo; ex. -1)'); ap.add_argument('--max', type=float, default=2.0)
A = ap.parse_args()
assert A.db <= 0 and -A.db <= A.max, f'ganho {A.db} dB fora da regra (0 a -{A.max} dB)'
assert A.entrada != A.saida, 'saída tem que ser outro arquivo'
def medir(f):
    e = subprocess.run(['ffmpeg', '-nostats', '-i', f, '-vn', '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    tp = re.findall(r'Peak:\s+(-?[\d.]+|-inf) dBFS', e); i = re.findall(r'I:\s+(-?[\d.]+) LUFS', e)
    return dict(true_peak_dbtp=float(tp[-1]) if tp else None, lufs=float(i[-1]) if i else None)
antes = medir(A.entrada)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', A.entrada, '-map', '0:v:0', '-map', '0:a:0', '-c:v', 'copy', '-af', f'volume={A.db}dB',
                '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-movflags', '+faststart', '-tag:v', 'hvc1', A.saida], check=True)
depois = medir(A.saida)
print(json.dumps(dict(entrada=A.entrada, saida=A.saida, db=A.db, antes=antes, depois=depois), ensure_ascii=False, indent=1))
if depois['true_peak_dbtp'] is not None and depois['true_peak_dbtp'] > -1.0: print('ATENÇÃO: true peak ainda acima de -1 dBTP', file=sys.stderr)
