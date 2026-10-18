# Transcreve só as tomadas candidatas a gancho, offline (faster-whisper large-v3 int8, HF_HUB_OFFLINE=1), com tempo por palavra.
# Serve para conferir as palavras literais e os limites de cada tomada (entrada do cortes_tomadas.py e da legenda do gancho).
# Uso: python3 transcrever_tomadas.py --bruto bruto.mp4 --prefixo ep4 --tomada B:192.18:196.28 --tomada C:201.58:206.84 \
#          --saida analise/tomadas/large-v3.json [--pasta-wav analise/tomadas] [--modelo large-v3] [--threads 4]
#   Os tempos de --tomada são aproximados (segundos no bruto), achados na transcrição geral do bruto; o recorte leva 1 s de folga de cada lado.
# Saída: JSON {"ep4-B": [[ini, fim, "palavra"], ...], ...} em segundos do bruto. Se o arquivo já existe, as chaves novas são somadas.
import json, subprocess, os, argparse
from pathlib import Path
os.environ.setdefault('HF_HUB_OFFLINE', '1')
ap = argparse.ArgumentParser(description='transcrição por palavra das tomadas de gancho')
ap.add_argument('--bruto', required=True); ap.add_argument('--prefixo', required=True, help='ex.: ep4 (vira ep4-B, ep4-C...)')
ap.add_argument('--tomada', action='append', required=True, help='NOME:ini:fim em segundos do bruto (repita)')
ap.add_argument('--saida', required=True); ap.add_argument('--pasta-wav'); ap.add_argument('--modelo', default='large-v3'); ap.add_argument('--threads', type=int, default=4)
A = ap.parse_args()
from faster_whisper import WhisperModel
PW = Path(A.pasta_wav or Path(A.saida).parent); PW.mkdir(parents=True, exist_ok=True)
m = WhisperModel(A.modelo, device='cpu', compute_type='int8', cpu_threads=A.threads)
out = json.loads(Path(A.saida).read_text()) if Path(A.saida).exists() else {}
for t in A.tomada:
    i, a, b = t.split(':'); a, b = float(a), float(b); s0 = max(0.0, a - 1.0)
    w = PW / f'{A.prefixo}-{i}.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(s0), '-t', str(b - s0 + 1.0), '-i', A.bruto, '-vn', '-ac', '1', '-ar', '16000', str(w)], check=True)
    segs, _ = m.transcribe(str(w), language='pt', word_timestamps=True, beam_size=5, condition_on_previous_text=False)
    ws = [(round(x.start + s0, 2), round(x.end + s0, 2), x.word.strip()) for s in segs for x in s.words]
    out[f'{A.prefixo}-{i}'] = ws
    print(A.prefixo, i, ' '.join(x[2] for x in ws), flush=True)
Path(A.saida).parent.mkdir(parents=True, exist_ok=True)
Path(A.saida).write_text(json.dumps(out, ensure_ascii=False, indent=1))
