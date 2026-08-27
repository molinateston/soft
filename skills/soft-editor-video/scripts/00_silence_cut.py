#!/usr/bin/env python3
"""Corta silêncios, aplica fades de 30 ms e grava o mapa explícito de cortes.

Uso:
  python3 00_silence_cut.py entrada.mp4 saida.mp4 [noise_dB] [dur_min]
      [--manifest edit-manifest.json]
"""
import argparse
import json
import os
import re
import subprocess
import sys

FADE_SECONDS = 0.030


def parse_args(argv=None):
    raw = list(sys.argv[1:] if argv is None else argv)
    if len(raw) >= 3 and re.fullmatch(r"-\d+(?:\.\d+)?dB", raw[2]):
        raw[2] = f"--noise={raw[2]}"
    parser = argparse.ArgumentParser()
    parser.add_argument("src")
    parser.add_argument("out")
    parser.add_argument("noise_pos", nargs="?", default=None)
    parser.add_argument("dur_min", nargs="?", default="0.35")
    parser.add_argument("--noise", dest="noise_opt", default=None)
    parser.add_argument("--manifest")
    args = parser.parse_args(raw)
    if args.noise_opt and args.noise_pos and args.dur_min == "0.35":
        args.dur_min = args.noise_pos
        args.noise_pos = None
    args.noise = args.noise_opt or args.noise_pos or "-30dB"
    return args


def probe_duration(src):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
         "default=noprint_wrappers=1:nokey=1", src],
        capture_output=True, text=True, check=True,
    )
    return float(result.stdout.strip())


def detect_keep_segments(src, duration, noise, dur_min, pad=0.10):
    result = subprocess.run(
        ["ffmpeg", "-i", src, "-af", f"silencedetect=noise={noise}:d={dur_min}",
         "-f", "null", "-"],
        capture_output=True, text=True,
    )
    starts = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", result.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", result.stderr)]
    silences = [(start + pad, end - pad) for start, end in zip(starts, ends)
                if end - pad > start + pad]
    keep = []
    cursor = 0.0
    for start, end in silences:
        if start > cursor:
            keep.append((cursor, start))
        cursor = end
    if cursor < duration:
        keep.append((cursor, duration))
    return [(start, end) for start, end in keep if end - start > 0.08]


def build_filter(keep):
    chains = []
    concat_inputs = []
    for index, (start, end) in enumerate(keep):
        segment_duration = end - start
        fade_out_start = segment_duration - FADE_SECONDS
        chains.append(
            f"[0:v]trim=start={start:.6f}:end={end:.6f},setpts=PTS-STARTPTS[v{index}]"
        )
        chains.append(
            f"[0:a]atrim=start={start:.6f}:end={end:.6f},asetpts=PTS-STARTPTS,"
            f"afade=t=in:st=0:d={FADE_SECONDS:.3f},"
            f"afade=t=out:st={fade_out_start:.6f}:d={FADE_SECONDS:.3f}[a{index}]"
        )
        concat_inputs.append(f"[v{index}][a{index}]")
    chains.append("".join(concat_inputs) + f"concat=n={len(keep)}:v=1:a=1[v][a]")
    return ";".join(chains)


def cut_map(keep):
    timeline_cursor = 0.0
    mapped = []
    for index, (source_start, source_end) in enumerate(keep, 1):
        duration = source_end - source_start
        mapped.append({
            "id": f"cut-{index:03d}",
            "source_start": round(source_start, 6),
            "source_end": round(source_end, 6),
            "timeline_start": round(timeline_cursor, 6),
            "timeline_end": round(timeline_cursor + duration, 6),
            "audio_fade_in_ms": 30,
            "audio_fade_out_ms": 30,
        })
        timeline_cursor += duration
    return mapped


def update_manifest(path, keep, source_duration):
    data = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
    mapped = cut_map(keep)
    timeline_duration = sum(end - start for start, end in keep)
    data["speech_compaction"] = {
        "source_duration": round(source_duration, 6),
        "timeline_duration": round(timeline_duration, 6),
        "removed_duration": round(source_duration - timeline_duration, 6),
        "word_timed": True,
    }
    data["cut_map"] = mapped
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def main(argv=None):
    args = parse_args(argv)
    duration = probe_duration(args.src)
    keep = detect_keep_segments(args.src, duration, args.noise, args.dur_min)
    if not keep:
        print("FALHA: nenhum trecho de fala preservado", file=sys.stderr)
        return 1
    new_duration = sum(end - start for start, end in keep)
    print(
        f"orig={duration:.2f}s newdur={new_duration:.2f}s "
        f"cortado={duration - new_duration:.2f}s cortes={max(0, len(keep) - 1)}",
        flush=True,
    )
    result = subprocess.run(
        ["ffmpeg", "-y", "-i", args.src, "-filter_complex", build_filter(keep),
         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "fast",
         "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
         args.out],
        capture_output=True,
    )
    if result.returncode != 0:
        print("FALHA: corte não exportado", file=sys.stderr)
        print(result.stderr.decode(errors="replace")[-1200:], file=sys.stderr)
        return result.returncode
    if args.manifest:
        update_manifest(args.manifest, keep, duration)
    print(f"PASSA: corte exportado com fades de 30 ms em {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
