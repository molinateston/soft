"""Anima localmente cada imagem _16x9.jpg com movimento curto de 3 segundos.
Uso: python3 02_animate.py /pasta_img /pasta_video
"""
import os, sys, glob, subprocess
sys.path.insert(0, os.path.dirname(__file__))
import _config as C

if len(sys.argv) < 2:
    print("uso: python3 02_animate.py /pasta_img /pasta_video")
    raise SystemExit(2)
IMGDIR = sys.argv[1]
VIDDIR = sys.argv[2] if len(sys.argv) > 2 else os.path.join(C.OUTPUT_DIR, "video")
os.makedirs(VIDDIR, exist_ok=True)
def run(img):
    wid = os.path.basename(img).replace("_16x9.jpg","")
    out = f"{VIDDIR}/{wid}.mp4"
    vf = (
        "scale=1200:675:force_original_aspect_ratio=increase,crop=1200:675,"
        "zoompan=z='min(zoom+0.0008,1.06)':x='iw/2-(iw/zoom/2)':"
        "y='ih/2-(ih/zoom/2)':d=90:s=1080x608:fps=30,format=yuv420p"
    )
    done = subprocess.run(
        ["ffmpeg", "-y", "-loop", "1", "-i", img, "-vf", vf, "-t", "3",
         "-an", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", out],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    if done.returncode != 0 or not os.path.exists(out) or os.path.getsize(out) == 0:
        print("FALHA:", wid)
        return False
    print("MOVIMENTO CRIADO", wid, flush=True)
    return True

images = sorted(glob.glob(f"{IMGDIR}/*_16x9.jpg"))
results = [run(img) for img in images]
if not results or not all(results):
    raise SystemExit(1)
print("PASSA: todos os movimentos existem ->", VIDDIR)
