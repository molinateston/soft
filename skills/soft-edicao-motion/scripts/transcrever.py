"""Transcrição local com tempo por palavra (faster-whisper), em Linux, Mac e Windows.

Grava no formato que os scripts da skill leem: {"words": [{text,start,end}], "audio_duration_secs"}.
Uso: python transcrever.py <midia> <saida.json> [--model PASTA_OU_TAMANHO] [--lang pt]
Modelo padrão: "medium" (ou a variável WHISPER_MODEL). Em máquina sem placa de vídeo, "small" é bem mais rápido.
"""
import argparse, glob, json, os, sys, site


def add_cuda_dlls():
    # Só o Windows precisa apontar as DLLs da CUDA instaladas pelo pip; nos outros sistemas não faz nada.
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
    ap.add_argument("--model", default=os.environ.get("WHISPER_MODEL", "medium"))
    ap.add_argument("--lang", default="pt")
    a = ap.parse_args()

    add_cuda_dlls()
    from faster_whisper import WhisperModel

    try:
        model = WhisperModel(a.model, device="cuda", compute_type="float16")
        device = "cuda"
    except Exception as e:  # sem placa de vídeo utilizável
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
    print(f"FEITO device={device} palavras={len(words)} -> {a.out}")


if __name__ == "__main__":
    main()
