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
    diff = ImageChops.difference(Image.open(a).convert("RGB").crop(box), Image.open(b).convert("RGB").crop(box))
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
    if (v.get("width"), v.get("height")) != (720, 1280): errors.append("dimensões diferentes de 720x1280")
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
        roi = (80, call_y - 10, 640, min(1280, call_y + 100))
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
