"""
MOTION EDITS PRO - transcribe.py
Transcribe un crudo SIN internet de modelos (Hugging Face suele estar bloqueado): usa Whisper en formato
sherpa-onnx, que se baja de GitHub Releases. Luego estima el tiempo de cada palabra
(sincronia aproximada: error < 1 s) con la envolvente de energia de la voz.

    python3 transcribe.py crudo.mp4 --out work/words.json
        -> imprime la transcripcion cruda por tramos (revisarla y corregir nombres propios)
    python3 transcribe.py crudo.mp4 --out work/words.json --text work/texto_corregido.txt
        -> alinea el texto corregido y escribe words.json = [[palabra, t_ini, t_fin], ...]

Despues de corregir, mostrarle la transcripcion al usuario.
"""
import argparse, json, os, re, subprocess, sys, tarfile, urllib.request
import numpy as np

MODEL_URL = 'https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-small.tar.bz2'
MODEL_DIR = os.path.expanduser('~/.cache/motion-edits-pro')


def ensure_model():
    d = os.path.join(MODEL_DIR, 'sherpa-onnx-whisper-small')
    if os.path.exists(os.path.join(d, 'small-encoder.int8.onnx')):
        return d
    os.makedirs(MODEL_DIR, exist_ok=True)
    tgz = os.path.join(MODEL_DIR, 'w.tar.bz2')
    print('bajando modelo (~640 MB) desde GitHub...', file=sys.stderr)
    urllib.request.urlretrieve(MODEL_URL, tgz)
    with tarfile.open(tgz) as t: t.extractall(MODEL_DIR)
    os.remove(tgz)
    return d


def load_wav(path, sr=16000):
    import soundfile as sf
    import tempfile
    wav = os.path.join(tempfile.gettempdir(), '_mep_%d_%s.wav' % (os.getpid(), os.urandom(4).hex()))   # nome unico: varios processos ao mesmo tempo
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', path, '-ar', str(sr), '-ac', '1', wav], check=True)
    x, s = sf.read(wav, dtype='float32'); os.remove(wav)
    return x, s


def envelope(x, sr, hop=.01):
    from scipy.signal import butter, sosfiltfilt
    y = sosfiltfilt(butter(4, [200, 3500], btype='band', fs=sr, output='sos'), x)
    h = int(hop * sr)
    env = np.array([np.sqrt(np.mean(y[i:i + h * 2] ** 2)) for i in range(0, len(y) - h * 2, h)])
    return np.convolve(env, np.ones(5) / 5, 'same')


def chunk_bounds(env, dur, target=22.0):
    """cortes de ~target s, ubicados en el minimo de energia (pausa) +-2 s."""
    b, t = [0.0], target
    while t < dur - 6:
        a, z = int((t - 2) * 100), int((t + 2) * 100)
        b.append(round((a + int(np.argmin(env[a:z]))) / 100, 2))
        t = b[-1] + target
    b.append(dur)
    return list(zip(b[:-1], b[1:]))


def transcribe(path, lang='es'):
    import sherpa_onnx
    d = ensure_model()
    r = sherpa_onnx.OfflineRecognizer.from_whisper(
        encoder=d + '/small-encoder.int8.onnx', decoder=d + '/small-decoder.int8.onnx',
        tokens=d + '/small-tokens.txt', language=lang, task='transcribe', num_threads=4)
    x, sr = load_wav(path)
    env = envelope(x, sr)
    out = []
    for a, b in chunk_bounds(env, len(x) / sr):
        st = r.create_stream(); st.accept_waveform(sr, x[int(a * sr):int(b * sr)]); r.decode_stream(st)
        out.append((a, b, st.result.text.strip()))
    return out, x, sr, env


SPECIAL = {}  # {'skill': 1, 'remotion': 3, ...} silabas de palabras en ingles/marcas

def _syl(w):
    w = re.sub(r'[^a-záéíóúüñ]', '', w.lower())
    return SPECIAL.get(w, len(re.findall(r'[aeiouáéíóú]+', w)) or 1)


def align(text, env):
    """reparte las palabras en el tiempo segun silabas y energia de voz. Devuelve [[w, t0, t1], ...]"""
    words = re.findall(r"[\wáéíóúüñÁÉÍÓÚÜÑ]+", text)
    act = np.clip(env - np.percentile(env, 25), 0, None)
    cum = np.cumsum(act); cum /= cum[-1]
    cs = np.cumsum([_syl(w) for w in words]); cs = cs / cs[-1]
    out = []
    for w, c0, c1 in zip(words, np.concatenate([[0], cs[:-1]]), cs):
        out.append([w, round(float(np.searchsorted(cum, c0)) * .01, 2), round(float(np.searchsorted(cum, c1)) * .01, 2)])
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('video'); ap.add_argument('--out', default='words.json')
    ap.add_argument('--text', help='archivo con el texto corregido para alinear')
    ap.add_argument('--lang', default='es')
    a = ap.parse_args()
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    if a.text:
        x, sr = load_wav(a.video); env = envelope(x, sr)
        w = align(open(a.text, encoding='utf-8').read(), env)
        json.dump(w, open(a.out, 'w'), ensure_ascii=False)
        print(f'{len(w)} palabras alineadas -> {a.out}')
    else:
        chunks, x, sr, env = transcribe(a.video, a.lang)
        for s, e, t in chunks: print(f'[{s:5.1f}-{e:5.1f}] {t}')
