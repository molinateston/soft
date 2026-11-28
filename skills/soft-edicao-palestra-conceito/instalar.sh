#!/usr/bin/env bash
# Instala as dependencias da skill (Linux/Debian/Ubuntu; no macOS troque apt por brew install ffmpeg).
set -e
cd "$(dirname "$0")"
if ! command -v ffmpeg >/dev/null; then sudo apt-get update && sudo apt-get install -y ffmpeg; fi
python3 -m pip install -r requirements.txt
python3 -c "import faster_whisper, cv2, numpy, scipy, PIL; print('dependencias ok')"
ffmpeg -hide_banner -version | head -1
# o modelo do whisper (large-v3, ~3 GB) baixa sozinho na primeira transcricao
