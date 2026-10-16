"""Transcrição local com tempo por palavra (faster-whisper). Roda em Linux, Mac e Windows.

Grava o formato que os scripts desta skill leem:
  {"words": [{"text", "start", "end"}], "audio_duration_secs", "language_code", "text"}
Uso: python transcrever.py <video_ou_audio> <saida.json> [--model small|medium|PASTA] [--lang pt]
Instalação (uma vez): python -m venv ~/.venvs/whisper e depois
  ~/.venvs/whisper/bin/pip install faster-whisper   (no Windows: ~/.venvs/whisper/Scripts/pip)
GPU NVIDIA é usada se existir; sem ela roda na CPU (mais lento, mesmo resultado).
"""
import argparse
import glob
import json
import os
import site
import sys


def libera_dll_cuda():
    """Só no Windows: aponta as DLLs CUDA instaladas pelo pip. Nos outros sistemas não faz nada."""
    if not hasattr(os, "add_dll_directory"):
        return
    for base in site.getsitepackages():
        for d in glob.glob(os.path.join(base, "nvidia", "*", "bin")):
            os.add_dll_directory(d)
            os.environ["PATH"] = d + os.pathsep + os.environ["PATH"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("media")
    ap.add_argument("out")
    ap.add_argument("--model", default=os.environ.get("WHISPER_MODEL", "small"))
    ap.add_argument("--lang", default="pt")
    a = ap.parse_args()

    libera_dll_cuda()
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("faster-whisper não instalado neste python. Veja 'Primeiros passos' no SKILL.md.", file=sys.stderr)
        sys.exit(2)

    try:
        model = WhisperModel(a.model, device="cuda", compute_type="float16")
        device = "cuda"
    except Exception as e:  # sem GPU utilizável
        print(f"cuda indisponível ({e}); usando cpu", file=sys.stderr)
        model = WhisperModel(a.model, device="cpu", compute_type="int8")
        device = "cpu"

    segments, info = model.transcribe(
        a.media, language=a.lang, word_timestamps=True, vad_filter=False,
        condition_on_previous_text=False,
    )
    words = []
    for seg in segments:
        for w in seg.words or []:
            words.append({"text": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)})
        print(f"[{seg.start:7.2f}] {seg.text.strip()}", flush=True)

    with open(a.out, "w", encoding="utf-8") as f:
        json.dump({"language_code": a.lang, "audio_duration_secs": round(info.duration, 3),
                   "text": " ".join(w["text"] for w in words), "words": words}, f, ensure_ascii=False, indent=1)
    print(f"PRONTO device={device} palavras={len(words)} -> {a.out}")


if __name__ == "__main__":
    main()
