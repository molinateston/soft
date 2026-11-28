"""Etapa 2. Transcricao com tempo por palavra (faster-whisper), em tempo ABSOLUTO da fonte.
Modelo, idioma e prompt (nomes proprios do cliente) vem de marca.json > whisper.
uso: python3 02_transcrever.py TRAB [audio.wav saida.json offset]
sem argumentos extras: transcreve TRAB/fonte16.wav -> TRAB/transcricao.json (+ trechos.txt para escolher cortes)
com argumentos: transcreve qualquer wav (o gate de fala usa isso no audio do final)."""
import json, os, sys, hashlib
from importlib.metadata import version
import comum as C

T = C.trab_arg()
M = C.marca(T)
Wh = M['whisper']
if len(sys.argv) > 2:
    wav, out, off = sys.argv[2], sys.argv[3], float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
else:
    wav, out, off = os.path.join(T, 'fonte16.wav'), os.path.join(T, 'transcricao.json'), C.lj(T, 'entrada.json')['offset']
# Cache identificado pelo áudio, configuração, offset e versão do motor. Nunca só existência.
def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for bloco in iter(lambda: f.read(1024 * 1024), b''):
            h.update(bloco)
    return h.hexdigest()
meta_path = out + '.cache.json'
identidade = dict(audio_sha256=sha(wav), whisper=Wh, offset=off,
                  motor=version('faster-whisper'), esquema=1)
if os.path.exists(out) and os.path.exists(meta_path):
    try:
        meta = json.load(open(meta_path))
        textos_ok = len(sys.argv) > 2 or os.path.exists(os.path.join(T, 'trechos.txt'))
        if meta.get('identidade') == identidade and meta.get('saida_sha256') == sha(out) and textos_ok:
            print('PRONTO cache coerente ->', out)
            sys.exit(0)
    except (ValueError, OSError):
        pass
from faster_whisper import WhisperModel

# maquina sobrecarregada (load > nucleos): 1 thread; com 4 o CTranslate2 fica girando em espera e nao anda
THR = int(os.environ.get('THREADS') or (1 if os.getloadavg()[0] > (os.cpu_count() or 4) else 4))
m = WhisperModel(Wh.get('modelo', 'large-v3'), device='cpu', compute_type='int8', cpu_threads=THR)
segs, _ = m.transcribe(wav, language=Wh.get('idioma', 'pt'), word_timestamps=True, vad_filter=False, beam_size=int(Wh.get('beam', 5)),
                       condition_on_previous_text=False, initial_prompt=Wh.get('prompt') or None)
S = []
for s in segs:
    S.append(dict(t0=round(s.start + off, 3), t1=round(s.end + off, 3), texto=s.text.strip(),
                  palavras=[dict(t0=round(w.start + off, 3), t1=round(w.end + off, 3), w=w.word.strip(), p=round(w.probability, 3)) for w in s.words]))
    print(f'{s.start + off:8.2f} {s.end + off:8.2f} {s.text.strip()}', flush=True)
json.dump(dict(segmentos=S), open(out, 'w'), ensure_ascii=False, indent=1)
if len(sys.argv) <= 2:
    with open(os.path.join(T, 'trechos.txt'), 'w') as f:
        for s in S:
            f.write(f"{s['t0']:8.2f} {s['t1']:8.2f}  {s['texto']}\n")
n = sum(len(s['palavras']) for s in S)
if not n:
    sys.exit('FALHOU: nenhuma palavra; cache não publicado')
with open(meta_path + '.novo', 'w') as f:
    json.dump(dict(identidade=identidade, saida_sha256=sha(out)), f, ensure_ascii=False, indent=2)
os.replace(meta_path + '.novo', meta_path)
print('PRONTO' if n else 'FALHOU: nenhuma palavra', f'{len(S)} segmentos, {n} palavras ->', out)
