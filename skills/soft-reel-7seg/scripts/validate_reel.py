#!/usr/bin/env python3
import argparse
import json
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageChops


def capture(video, at, target):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-ss", str(at), "-i", str(video), "-frames:v", "1", str(target), "-y"], check=True)


def changed_pixels(a, b, box, threshold=40):
    first = Image.open(a).convert("RGB")
    second = Image.open(b).convert("RGB")
    # O arquivo-base pode ter dimensão diferente da exportada; alinhe antes de comparar.
    if second.size != first.size:
        second = second.resize(first.size)
    diff = ImageChops.difference(first.crop(box), second.crop(box))
    return sum(1 for pixel in diff.getdata() if max(pixel) > threshold)


def main():
    p = argparse.ArgumentParser(description="Valida safe zone, chamada tardia, mídia e quatro quadros de um Reel.")
    p.add_argument("--video", required=True)
    p.add_argument("--manifest", required=True)
    p.add_argument("--frames-dir", required=True)
    args = p.parse_args()
    video = Path(args.video)
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    probe = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration,size:stream=codec_name,codec_type,width,height,sample_rate,channels", "-of", "json", str(video)]))
    streams = probe["streams"]
    v = next(s for s in streams if s["codec_type"] == "video")
    a = next((s for s in streams if s["codec_type"] == "audio"), None)
    errors = []
    width, height = int(v.get("width") or 0), int(v.get("height") or 0)
    # Vertical 9:16, e nunca abaixo da resolução do arquivo-base: exportar menor
    # que a fonte joga resolução fora sem necessidade.
    if not width or not height:
        errors.append("não foi possível ler a dimensão do vídeo")
    elif abs(width * 16 - height * 9) > max(2, height * 0.01):
        errors.append(f"não é vertical 9:16: {width}x{height}")
    base = manifest.get("base")
    if base and width and height:
        base_probe = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "json", str(base)]))
        bs = base_probe["streams"][0]
        base_h = int(bs.get("height") or 0)
        if base_h and height < base_h:
            errors.append(f"saída {width}x{height} abaixo da fonte {bs.get('width')}x{base_h}")
    if v.get("codec_name") != "h264": errors.append("vídeo não está em H.264")
    if not a or a.get("codec_name") != "aac": errors.append("áudio não está em AAC")
    if abs(float(probe["format"]["duration"]) - float(manifest["duration"])) > 0.03: errors.append("duração fora da tolerância")
    if int(probe["format"]["size"]) >= int(manifest["max_bytes"]): errors.append("arquivo excede o limite")
    if manifest["face_gap"] < manifest["min_face_gap"]: errors.append("safe zone facial insuficiente")

    frames_dir = Path(args.frames_dir)
    frames_dir.mkdir(parents=True, exist_ok=True)
    duration = float(manifest["duration"])
    times = [min(0.35, duration * .1), duration * .37, min(float(manifest["call_time"]) + .28, duration * .7), duration * .93]
    frames = []
    for index, at in enumerate(times, 1):
        target = frames_dir / f"quadro-{index:02d}-{at:.2f}s.png"
        capture(video, at, target)
        frames.append(target)
    subprocess.run(["montage", *map(str, frames), "-tile", "2x2", "-geometry", "360x640+4+4", str(frames_dir / "mosaico.jpg")], check=True)

    with tempfile.TemporaryDirectory(prefix="validate-reel-") as tmp:
        t = Path(tmp)
        before = max(0.05, float(manifest["call_time"]) - 0.12)
        after = min(duration - 0.05, float(manifest["call_time"]) + 0.12)
        files = {}
        for label, source, at in (("ob", video, before), ("bb", manifest["base"], before), ("oa", video, after), ("ba", manifest["base"], after)):
            files[label] = t / f"{label}.png"
            capture(source, at, files[label])
        call_y = int(manifest["call_y"])
        # A janela de leitura acompanha a dimensão real do arquivo, em vez de
        # coordenadas cravadas de uma resolução só.
        escala = height / 1280 if height else 1
        margem = int(80 * escala)
        roi = (margem, call_y - int(10 * escala), max(margem + 1, width - margem),
               min(height, call_y + int(100 * escala)))
        before_pixels = changed_pixels(files["ob"], files["bb"], roi)
        after_pixels = changed_pixels(files["oa"], files["ba"], roi)
        if before_pixels > 400: errors.append(f"microchamada aparece cedo: {before_pixels} pixels")
        if after_pixels < 800: errors.append(f"microchamada não foi detectada depois da entrada: {after_pixels} pixels")

    result = {
        "ok": not errors, "errors": errors, "dimensions": [v.get("width"), v.get("height")],
        "video_codec": v.get("codec_name"), "audio_codec": a.get("codec_name") if a else None,
        "duration": float(probe["format"]["duration"]), "size": int(probe["format"]["size"]),
        "face_gap": manifest["face_gap"], "call_before_pixels": before_pixels,
        "call_after_pixels": after_pixels, "mosaic": str((frames_dir / "mosaico.jpg").resolve())
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if errors: raise SystemExit(1)


if __name__ == "__main__":
    main()
