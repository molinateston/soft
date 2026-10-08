"""Tiempos REALES de palabras de la voz (la alineacion por silabas de transcribe.py llega a errar ~1.5 s).
Metodo: (1) tramos de voz y picos silabicos por energia; (2) Whisper (sherpa-onnx) sobre PREFIJOS crecientes del audio
para ver en que instante aparece cada palabra.
    python3 align_voice.py crudo.mp4 segmentos   -> tramos de voz + picos (rapido)
    python3 align_voice.py crudo.mp4 prefijos 9.0,9.5,10.0,10.5 8.4   -> texto transcripto de [8.4, fin] para cada fin (lento, ~10 s c/u: <= 8 por llamada)
Usar siempre estos tiempos para anclar eventos; verificar con stills."""
import sys, os, subprocess, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
def load(path, sr=16000):
    import soundfile as sf, tempfile
    wav = os.path.join(tempfile.gettempdir(), '_al_%d_%s.wav' % (os.getpid(), os.urandom(4).hex()))   # nome unico: varios processos ao mesmo tempo
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', path, '-ar', str(sr), '-ac', '1', wav], check=True)
    out = sf.read(wav, dtype='float32'); os.remove(wav); return out
def segmentos(path):
    from scipy.signal import butter, sosfiltfilt, find_peaks
    x, sr = load(path)
    y = sosfiltfilt(butter(4, [150, 3000], btype='band', fs=sr, output='sos'), x); hop = int(.005 * sr)
    env = np.array([np.sqrt(np.mean(y[i:i + hop * 4] ** 2)) for i in range(0, len(y) - hop * 4, hop)])
    env = np.convolve(env, np.ones(5) / 5, 'same'); env /= env.max(); t = np.arange(len(env)) * .005
    act = env > .05; segs = []; s = None
    for i, a in enumerate(act):
        if a and s is None: s = i
        if not a and s is not None:
            if t[i] - t[s] > .05: segs.append((round(t[s], 2), round(t[i], 2)))
            s = None
    sm = np.convolve(env, np.ones(9) / 9, 'same'); pk, _ = find_peaks(sm, distance=int(.11 / .005), prominence=.04)
    print('TRAMOS DE VOZ:', ' | '.join(f'{a}-{b}' for a, b in segs)); print('PICOS SILABICOS:', [round(float(t[i]), 2) for i in pk])
def prefijos(path, ends, start):
    import transcribe as T, sherpa_onnx
    d = T.ensure_model()
    r = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=d + '/small-encoder.int8.onnx', decoder=d + '/small-decoder.int8.onnx', tokens=d + '/small-tokens.txt', language='es', task='transcribe', num_threads=4)
    x, sr = load(path)
    for e in ends:
        st = r.create_stream(); st.accept_waveform(sr, x[int(start * sr):int(e * sr)]); r.decode_stream(st); print(f'{e:.2f} | {st.result.text.strip()}', flush=True)
if __name__ == '__main__':
    if sys.argv[2] == 'segmentos': segmentos(sys.argv[1])
    else: prefijos(sys.argv[1], [float(v) for v in sys.argv[3].split(',')], float(sys.argv[4]) if len(sys.argv) > 4 else 0.0)
