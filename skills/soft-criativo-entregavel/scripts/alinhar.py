"""Tempos reais da fala: transcreve prefixos crescentes de cada frase (Whisper) para ver em que instante cada palavra aparece.
    python alinhar.py <audio> <inicios das frases, em s, separados por virgula> [pasta_do_criativo]
Os inicios vem dos BLOCOS DE FALA de analisar_audio.py (um por frase; dividir frases longas a cada ~3 s).
Cada linha da saida e "inicio -> fim | texto ouvido ate ali": a palavra foi dita no primeiro 'fim' em que ela aparece.
Linhas com [Musica]/[Som] sao falhas do reconhecedor naquele prefixo: ignorar e olhar as vizinhas.
Grava alinhamento.txt na pasta do criativo, se dada.
"""
import sys, os, tempfile
import numpy as np
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
STEP = .3
_R = None; _X = None

def init(npy, sr):
    global _R, _X
    import transcribe as T, sherpa_onnx, numpy as np
    d = T.ensure_model()
    _R = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=d + '/small-encoder.int8.onnx', decoder=d + '/small-decoder.int8.onnx',
                                                    tokens=d + '/small-tokens.txt', language='pt', task='transcribe', num_threads=3)
    _X = (np.load(npy, mmap_mode='r'), sr)

def job(a):
    s, e = a; x, sr = _X
    st = _R.create_stream(); st.accept_waveform(sr, np.asarray(x[int(s * sr):int(e * sr)])); _R.decode_stream(st)
    return s, e, st.result.text.strip()

if __name__ == '__main__':
    path = sys.argv[1]; starts = sorted(float(v) for v in sys.argv[2].split(','))
    import align_voice as A
    x, sr = A.load(path); dur = len(x) / sr; starts.append(dur); jobs = []
    npy = os.path.join(tempfile.gettempdir(), '_alinhar_%d.npy' % os.getpid()); np.save(npy, x)
    for s, n in zip(starts[:-1], starts[1:]):
        e = s + .6
        while e < n + .35: jobs.append((s, round(min(e, dur), 2))); e += STEP
    lines = []
    with Pool(6, initializer=init, initargs=(npy, sr)) as p:
        for s, e, txt in p.imap(job, jobs): lines.append(f'{s:6.2f} -> {e:6.2f} | {txt}'); print(lines[-1], flush=True)
    os.remove(npy)
    if len(sys.argv) > 3: open(os.path.join(sys.argv[3], 'alinhamento.txt'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
