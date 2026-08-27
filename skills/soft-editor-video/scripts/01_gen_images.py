"""Gera imagens pela conta ChatGPT do Codex, sem chave OpenAI paga.

scenes.json (o agente escreve por vídeo):
[
  {"id":"w01","chars":["principal","mascote","cohost"],"pose":"...ação da cena...","extra":"...elementos/texto..."},
  ...
]
Uso: python3 01_gen_images.py scenes.json /pasta/saida_img
"""
import os, sys, json, subprocess
sys.path.insert(0, os.path.dirname(__file__))
import _config as C

if len(sys.argv) < 2:
    print("uso: python3 01_gen_images.py scenes.json /pasta/saida_img")
    raise SystemExit(2)
SCENES = json.load(open(sys.argv[1]))
OUTDIR = sys.argv[2] if len(sys.argv) > 2 else os.path.join(C.OUTPUT_DIR, "img")
os.makedirs(OUTDIR, exist_ok=True)
P = C.load_personagens()

def char_blocks(keys):
    out = []
    for k in keys:
        d = P["personagens"].get(k) or P.get("extras", {}).get(k)
        if d: out.append(d)
    return "\n\n".join(out)

def frame(scene):
    chars = scene.get("chars") or P.get("trio_sempre", list(P["personagens"].keys()))
    return f"""Landscape 16:9 cinematic frame, {P.get('estilo','cinematic 3D')}, a believable scene.

CHARACTERS (always present, consistent):
{char_blocks(chars)}

SCENE / ACTION:
{scene['pose']}

ADDITIONAL VISUAL ELEMENTS:
{scene.get('extra','')}

ENVIRONMENT: {P.get('ambiente','')}

COLOR PALETTE: {P.get('paleta','')}

{P.get('safe_area','Keep all characters/text in the central 70%; top and bottom 18% are environment only.')}"""

def gen(scene):
    raw = os.path.abspath(f"{OUTDIR}/{scene['id']}_raw.png")
    crop = os.path.abspath(f"{OUTDIR}/{scene['id']}_16x9.jpg")
    instruction = (
        "Use your built-in image_gen tool to generate: " + frame(scene) + ". "
        "Save the result to " + raw + ". Do not write any python or HTML."
    )
    run = subprocess.run(
        ["codex", "exec", "--skip-git-repo-check", "--sandbox", "workspace-write", instruction],
        cwd="/home/cloud", text=True, capture_output=True, timeout=900
    )
    if run.returncode != 0 or not os.path.exists(raw) or os.path.getsize(raw) == 0:
        print(f"FALHA: imagem {scene['id']} nao foi criada")
        return False
    crop_run = subprocess.run(
        ["ffmpeg", "-y", "-i", raw, "-vf",
         "scale=1536:1024:force_original_aspect_ratio=increase,crop=1536:864", crop],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    if crop_run.returncode != 0 or not os.path.exists(crop) or os.path.getsize(crop) == 0:
        print(f"FALHA: corte 16:9 da imagem {scene['id']}")
        return False
    print("IMAGEM CRIADA", scene["id"], flush=True)
    return True

results = [gen(scene) for scene in SCENES]
if not results or not all(results):
    raise SystemExit(1)
print("PASSA: todas as imagens existem ->", OUTDIR)
