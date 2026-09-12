#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path


script = Path(__file__).with_name("gerenciar_estado.py")
created = subprocess.run(["python3", str(script), "init", "cenario"], check=True, text=True, capture_output=True).stdout.strip()
path = Path(created)
initial = json.loads(path.read_text(encoding="utf-8"))
assert initial["completed"] == []
subprocess.run(["python3", str(script), "update", str(path), "inventario", "--saida", "pecas.json"], check=True, capture_output=True)
resumed = json.loads(subprocess.run(["python3", str(script), "show", str(path)], check=True, text=True, capture_output=True).stdout)
assert resumed["completed"] == ["inventario"]
assert resumed["saidas"]["inventario"] == "pecas.json"
print("3 cenarios passaram: inicio vazio, pecas registradas e retomada preservada")
