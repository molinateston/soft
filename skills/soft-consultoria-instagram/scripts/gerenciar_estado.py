#!/usr/bin/env python3
"""Cria, atualiza e consulta o ponto de retomada de uma consultoria."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path


def save(path: Path, data: dict) -> None:
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    temp.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="action", required=True)
    init = sub.add_parser("init")
    init.add_argument("slug")
    update = sub.add_parser("update")
    update.add_argument("path")
    update.add_argument("step")
    update.add_argument("--saida")
    show = sub.add_parser("show")
    show.add_argument("path")
    args = parser.parse_args()

    if args.action == "init":
        epoch = int(time.time())
        path = Path(f"/tmp/soft-consultoria-instagram-{args.slug}-{epoch}.json")
        data = {"skill": "soft-consultoria-instagram", "slug": args.slug, "completed": [], "saidas": {}}
        save(path, data)
        print(path)
        return

    path = Path(args.path)
    if not path.exists():
        raise SystemExit(f"ERRO: estado nao encontrado: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if args.action == "update":
        if args.step not in data["completed"]:
            data["completed"].append(args.step)
        if args.saida:
            data["saidas"][args.step] = args.saida
        save(path, data)
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
