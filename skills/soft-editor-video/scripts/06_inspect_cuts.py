#!/usr/bin/env python3
"""Extrai prova de cada emenda e pede inspeção visual antes da auditoria final."""
import argparse
import json
import os
import subprocess
import sys


def parse_args(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    parser.add_argument("manifest")
    parser.add_argument("out_dir")
    return parser.parse_args(argv)


def inspection_targets(cut_map):
    targets = []
    for cut in cut_map[1:]:
        targets.append((cut["id"], float(cut["timeline_start"])))
    return targets


def extract_contact_sheet(video, cut_id, at, out_dir):
    cut_dir = os.path.join(out_dir, cut_id)
    os.makedirs(cut_dir, exist_ok=True)
    frames = []
    for index, when in enumerate((max(0.0, at - 0.08), at, at + 0.08), 1):
        frame = os.path.join(cut_dir, f"frame-{index}.jpg")
        result = subprocess.run(
            ["ffmpeg", "-y", "-ss", f"{when:.6f}", "-i", video,
             "-frames:v", "1", "-q:v", "2", frame],
            capture_output=True,
        )
        if result.returncode != 0 or not os.path.isfile(frame):
            raise RuntimeError(f"não foi possível extrair a prova de {cut_id}")
        frames.append(frame)
    proof = os.path.abspath(os.path.join(cut_dir, "mosaico.jpg"))
    result = subprocess.run(
        ["ffmpeg", "-y", "-i", frames[0], "-i", frames[1], "-i", frames[2],
         "-filter_complex", "[0:v][1:v][2:v]hstack=inputs=3[v]", "-map", "[v]", proof],
        capture_output=True,
    )
    if result.returncode != 0 or not os.path.isfile(proof):
        raise RuntimeError(f"não foi possível montar a prova de {cut_id}")
    return proof


def review(proof, cut_id):
    proof_dir = os.path.dirname(proof)
    proof_name = os.path.basename(proof)
    prompt = (
        f"Olhe a imagem {proof_name}. Ela mostra três quadros, antes, durante e depois do corte "
        f"{cut_id}. Verifique se a emenda não tem quadro preto, duplicação, salto visual, "
        "flash acidental, legenda partida ou overlay quebrado. Responda na primeira linha "
        "somente PASSA ou REPROVA e depois dê o motivo curto."
    )
    result = subprocess.run(
        ["codex", "exec", "--skip-git-repo-check", "--sandbox", "workspace-write",
         f"--image={proof_name}", prompt],
        capture_output=True, text=True, cwd=proof_dir,
    )
    if result.returncode != 0:
        raise RuntimeError(f"visão indisponível no corte {cut_id}")
    response = result.stdout.strip()
    first_line = response.splitlines()[0].strip().upper() if response else ""
    return first_line == "PASSA", response


def save_results(manifest_path, manifest, results):
    manifest["cut_inspections"] = results
    with open(manifest_path, "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def main(argv=None):
    args = parse_args(argv)
    with open(args.manifest, encoding="utf-8") as handle:
        manifest = json.load(handle)
    cut_map = manifest.get("cut_map")
    if not isinstance(cut_map, list) or not cut_map:
        print("FALHA: mapa explícito de cortes ausente", file=sys.stderr)
        return 1
    os.makedirs(args.out_dir, exist_ok=True)
    results = []
    failed = False
    try:
        for cut_id, at in inspection_targets(cut_map):
            proof = extract_contact_sheet(args.video, cut_id, at, args.out_dir)
            passed, verdict = review(proof, cut_id)
            results.append({
                "cut_id": cut_id,
                "passed": passed,
                "proof": proof,
                "reviewer": "codex-oauth",
                "verdict": verdict,
            })
            failed = failed or not passed
    except RuntimeError as error:
        save_results(args.manifest, manifest, results)
        print(f"FALHA: {error}", file=sys.stderr)
        return 2
    save_results(args.manifest, manifest, results)
    if failed:
        print("FALHA: ao menos um corte reprovou na inspeção visual")
        return 1
    print(f"PASSA: {len(results)} cortes inspecionados visualmente")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
