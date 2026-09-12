#!/usr/bin/env python3
import argparse
import json
import subprocess
import tempfile
from pathlib import Path


def run(cmd):
    subprocess.run(cmd, check=True)


def main():
    p = argparse.ArgumentParser(description="Renderiza Reel vertical com HEADLINE em duas caixas e microchamada tardia.")
    p.add_argument("--base", required=True)
    p.add_argument("--audio", default=None, help="Arquivo que fornece a faixa de áudio final. Sem ele, o render segue com uma faixa silenciosa da duração do vídeo e declara isso no manifesto.")
    p.add_argument("--output", required=True)
    p.add_argument("--line1", required=True)
    p.add_argument("--line2", required=True)
    p.add_argument("--headline-y", type=int, required=True, help="Topo da primeira caixa em pixels.")
    p.add_argument("--face-top-y", type=int, required=True, help="Menor Y do cabelo no quadro crítico.")
    p.add_argument("--min-face-gap", type=int, default=32)
    p.add_argument("--font", default="/usr/share/fonts/opentype/inter/Inter-Black.otf")
    p.add_argument("--font-size", type=int, default=40)
    p.add_argument("--line-gap", type=int, default=0)
    p.add_argument("--call", default="Leia a descrição ↓")
    p.add_argument("--call-time", type=float, required=True)
    p.add_argument("--call-y", type=int, default=800)
    p.add_argument("--duration", type=float, required=True)
    p.add_argument("--max-mb", type=float, default=5.0)
    args = p.parse_args()

    for value in (args.base, args.font):
        if not Path(value).is_file():
            raise SystemExit(f"Arquivo ausente: {value}")
    # Vídeo sem fala É matéria-prima válida deste formato: o reel é headline sobre vídeo, e a
    # fala nunca foi obrigatória. Sem arquivo de áudio, o render NÃO para: entra uma faixa
    # silenciosa da mesma duração e o manifesto marca `audio_silencioso` pro handoff declarar.
    audio_silencioso = args.audio is None
    if not audio_silencioso and not Path(args.audio).is_file():
        raise SystemExit(f"Arquivo ausente: {args.audio}")
    line_height = args.font_size + 20
    headline_bottom = args.headline_y + 2 * line_height + args.line_gap
    face_gap = args.face_top_y - headline_bottom
    if face_gap < args.min_face_gap:
        raise SystemExit(f"Safe zone facial insuficiente: {face_gap}px; mínimo {args.min_face_gap}px")

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="reel-overlay-") as tmp:
        tmpdir = Path(tmp)
        text_files = []
        for index, text in enumerate((args.line1, args.line2, args.call), start=1):
            path = tmpdir / f"text-{index}.txt"
            path.write_text(text, encoding="utf-8")
            text_files.append(path)
        y1 = args.headline_y + 10
        y2 = args.headline_y + line_height + args.line_gap + 10
        filt = (
            f"[0:v]drawtext=fontfile='{args.font}':textfile='{text_files[0]}':fontsize={args.font_size}:"
            f"fontcolor=black:box=1:boxcolor=white:boxborderw=10:x=(w-text_w)/2:y={y1},"
            f"drawtext=fontfile='{args.font}':textfile='{text_files[1]}':fontsize={args.font_size}:"
            f"fontcolor=black:box=1:boxcolor=0x4ade80:boxborderw=10:x=(w-text_w)/2:y={y2},"
            f"drawtext=fontfile='{args.font}':textfile='{text_files[2]}':fontsize=28:fontcolor=black:"
            f"box=1:boxcolor=white:boxborderw=10:x=(w-text_w)/2:y={args.call_y + 10}:"
            f"enable='gte(t,{args.call_time})'[v]"
        )
        if audio_silencioso:
            entrada_audio = ["-f", "lavfi", "-t", f"{args.duration:.6f}",
                             "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]
        else:
            entrada_audio = ["-i", args.audio]
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", args.base, *entrada_audio,
             "-filter_complex", filt, "-map", "[v]", "-map", "1:a:0", "-c:v", "libx264",
             "-preset", "medium", "-crf", "23", "-pix_fmt", "yuv420p", "-c:a", "aac",
             "-b:a", "160k", "-t", f"{args.duration:.6f}", "-movflags", "+faststart", str(output), "-y"])

    size = output.stat().st_size
    if size >= args.max_mb * 1024 * 1024:
        raise SystemExit(f"Arquivo excede limite: {size} bytes")
    manifest = {
        "base": str(Path(args.base).resolve()), "output": str(output.resolve()),
        "headline": [args.line1, args.line2], "headline_y": args.headline_y,
        "headline_bottom": headline_bottom, "face_top_y": args.face_top_y,
        "face_gap": face_gap, "min_face_gap": args.min_face_gap,
        "call": args.call, "call_time": args.call_time, "call_y": args.call_y,
        "duration": args.duration, "max_bytes": int(args.max_mb * 1024 * 1024),
        "audio": str(Path(args.audio).resolve()) if args.audio else None,
        "audio_silencioso": audio_silencioso
    }
    output.with_suffix(output.suffix + ".json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()

