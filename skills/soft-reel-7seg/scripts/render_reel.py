#!/usr/bin/env python3
import argparse
import json
import subprocess
import tempfile
from PIL import ImageFont
from pathlib import Path


def run(cmd):
    subprocess.run(cmd, check=True)


def main():
    p = argparse.ArgumentParser(description="Renderiza Reel vertical nos caminhos A/B com layout legado, bloco ou texto limpo.")
    p.add_argument("--base", required=True)
    p.add_argument("--audio", default=None, help="Faixa externa final. Sem ela, auto preserva áudio-base ou declara silêncio quando não existe áudio.")
    p.add_argument("--output", required=True)
    p.add_argument("--line1", default="")
    p.add_argument("--line2", default="")
    p.add_argument("--headline-y", type=int, required=True, help="Topo da primeira caixa em pixels.")
    p.add_argument("--face-top-y", type=int, default=None, help="Menor Y do cabelo no quadro crítico.")
    p.add_argument("--min-face-gap", type=int, default=32)
    p.add_argument("--font", default="/usr/share/fonts/opentype/inter/Inter-Black.otf")
    p.add_argument("--font-size", type=int, default=40)
    p.add_argument("--line-gap", type=int, default=0)
    p.add_argument("--call", default="Leia a descrição ↓")
    p.add_argument("--call-time", type=float, default=None)
    p.add_argument("--call-y", type=int, default=800)
    p.add_argument("--duration", type=float, required=True)
    p.add_argument("--max-mb", type=float, default=5.0)
    p.add_argument("--path", choices=["A", "B"], default="A")
    p.add_argument("--layout", choices=["legacy", "block", "clean"], default="legacy")
    p.add_argument("--text-file", help="UTF-8: texto completo multilinha, preservado literalmente")
    p.add_argument("--no-call", action="store_true")
    p.add_argument("--audio-mode", choices=["auto", "preserve", "silent"], default="auto")
    args = p.parse_args()
    if not args.no_call and (args.call_time is None or not 0 < args.call_time < args.duration):
        p.error("Chamada exige --call-time entre zero e duração; ou use --no-call")
    if args.layout == "legacy" and (not args.line1 or not args.line2 or args.face_top_y is None):
        p.error("Layout legacy exige --line1, --line2 e --face-top-y")
    if args.layout != "legacy" and not args.text_file:
        p.error("Layout block/clean exige --text-file")
    text = Path(args.text_file).read_text(encoding="utf-8").strip() if args.text_file else args.line1 + "\n" + args.line2
    lines = text.splitlines()
    if any(len(line.split()) < 2 for line in lines):
        p.error("Cada linha precisa ter duas ou mais palavras; revise as quebras")
    probe = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_streams", "-of", "json", args.base]))
    v = next(x for x in probe["streams"] if x["codec_type"] == "video")
    width, height = int(v["width"]), int(v["height"])
    has_audio = any(x["codec_type"] == "audio" for x in probe["streams"])
    if args.audio_mode == "preserve" and (args.audio or not has_audio):
        p.error("preserve exige áudio-base e ausência de --audio")
    if args.audio_mode == "silent" and args.audio:
        p.error("silent não aceita --audio externo")

    for value in (args.base, args.font):
        if not Path(value).is_file():
            raise SystemExit(f"Arquivo ausente: {value}")
    audio_silencioso = args.audio_mode == "silent" or (not args.audio and not has_audio)
    if args.audio and not Path(args.audio).is_file():
        raise SystemExit(f"Arquivo ausente: {args.audio}")
    font = ImageFont.truetype(args.font, args.font_size)
    padding = 10 if args.layout != "clean" else 0
    line_height = args.font_size + 20
    text_width = max(font.getlength(line) for line in lines)
    headline_bottom = args.headline_y + len(lines) * line_height + args.line_gap
    face_gap = args.face_top_y - headline_bottom if args.face_top_y is not None else None
    if args.layout == "legacy" and face_gap < args.min_face_gap:
        raise SystemExit(f"Safe zone facial insuficiente: {face_gap}px")
    margin = (width - text_width) / 2 - padding
    if margin < 40 or args.headline_y < 0 or headline_bottom >= height:
        raise SystemExit("Texto fora da área segura: margem horizontal mínima 40px e bloco dentro do quadro")

    if args.duration <= 0:
        p.error("Duração precisa ser positiva")
    call_margin = None
    if not args.no_call:
        call_font = ImageFont.truetype(args.font, 28)
        call_margin = (width - call_font.getlength(args.call)) / 2 - 10
        if call_margin < 40 or args.call_y < 0 or args.call_y + 60 >= height:
            p.error("Chamada fora da área segura")
        if args.call_y < headline_bottom and args.call_y + 60 > args.headline_y:
            p.error("Chamada sobrepõe bloco de texto; ajuste --call-y")
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="reel-overlay-") as tmp:
        tmpdir = Path(tmp)
        text_files = []
        for index, overlay_text in enumerate((args.line1, args.line2, args.call), start=1):
            path = tmpdir / f"text-{index}.txt"
            path.write_text(overlay_text, encoding="utf-8")
            text_files.append(path)
        y1 = args.headline_y + 10
        y2 = args.headline_y + line_height + args.line_gap + 10
        if args.layout == "legacy":
            filt = (
            f"[0:v]drawtext=fontfile='{args.font}':textfile='{text_files[0]}':fontsize={args.font_size}:"
            f"fontcolor=black:box=1:boxcolor=white:boxborderw=10:x=(w-text_w)/2:y={y1},"
            f"drawtext=fontfile='{args.font}':textfile='{text_files[1]}':fontsize={args.font_size}:"
            f"fontcolor=black:box=1:boxcolor=0x4ade80:boxborderw=10:x=(w-text_w)/2:y={y2},"
            f"drawtext=fontfile='{args.font}':textfile='{text_files[2]}':fontsize=28:fontcolor=black:"
            f"box=1:boxcolor=white:boxborderw=10:x=(w-text_w)/2:y={args.call_y + 10}:"
            f"enable='gte(t,{args.call_time or 0})'[v]"
        )
        else:
            block = tmpdir / "block.txt"
            block.write_text(text, encoding="utf-8")
            style = "fontcolor=black:box=1:boxcolor=white:boxborderw=10" if args.layout == "block" else "fontcolor=white:shadowcolor=black:shadowx=2:shadowy=2"
            filt = f"[0:v]drawtext=fontfile='{args.font}':textfile='{block}':fontsize={args.font_size}:line_spacing=20:{style}:x=(w-text_w)/2:y={args.headline_y + 10}"
            if not args.no_call:
                filt += f",drawtext=fontfile='{args.font}':textfile='{text_files[2]}':fontsize=28:fontcolor=black:box=1:boxcolor=white:boxborderw=10:x=(w-text_w)/2:y={args.call_y + 10}:enable='gte(t,{args.call_time})'"
            filt += "[v]"
        if args.layout == "legacy" and args.no_call:
            filt = filt[:filt.rindex(",drawtext=")] + "[v]"
        if audio_silencioso:
            entrada_audio = ["-f", "lavfi", "-t", str(args.duration), "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]
            audio_map = "1:a:0"
        elif args.audio:
            entrada_audio = ["-i", args.audio]
            audio_map = "1:a:0"
        else:
            entrada_audio = []
            audio_map = "0:a:0"
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", args.base, *entrada_audio,
             "-filter_complex", filt, "-map", "[v]", "-map", audio_map, "-c:v", "libx264",
             "-preset", "medium", "-crf", "23", "-pix_fmt", "yuv420p", "-c:a", "aac",
             "-b:a", "160k", "-t", str(args.duration), "-movflags", "+faststart", str(output), "-y"])

    size = output.stat().st_size
    if size >= args.max_mb * 1024 * 1024:
        raise SystemExit(f"Arquivo excede limite: {size} bytes")
    manifest = {
        "base": str(Path(args.base).resolve()), "output": str(output.resolve()),
        "path": args.path, "layout": args.layout, "text": text, "headline": lines,
        "text_margin_left": margin, "text_margin_right": margin,
        "visual_review_required": "início, meio, fim, chamada: rosto, mãos, ação, contraste e leitura", "headline_y": args.headline_y,
        "headline_bottom": headline_bottom, "face_top_y": args.face_top_y,
        "face_gap": face_gap, "min_face_gap": args.min_face_gap,
        "call": None if args.no_call else args.call, "call_time": args.call_time, "call_y": args.call_y, "call_margin": call_margin,
        "duration": args.duration, "max_bytes": int(args.max_mb * 1024 * 1024),
        "audio": str(Path(args.audio).resolve()) if args.audio else None,
        "audio_silencioso": audio_silencioso, "audio_source": "silent" if audio_silencioso else ("external" if args.audio else "base")
    }
    output.with_suffix(output.suffix + ".json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()

