#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path


root = Path(__file__).resolve().parent.parent
keys = {
    "CLIENT", "DATE", "HERO_RESULT", "TWO_MINUTE_SUMMARY", "VISITOR_JOURNEY",
    "CENTRAL_DIAGNOSIS", "CURRENT_TO_FUTURE_SYSTEM", "FOUR_PROFILE_JOBS",
    "READY_TO_BUILD_SYSTEM", "EXECUTION_AND_FUTURE_STATE", "TECHNICAL_APPENDIX",
}
with tempfile.TemporaryDirectory() as directory:
    base = Path(directory)
    data = base / "data.json"
    output = base / "report.html"
    data.write_text(json.dumps({key: "teste" for key in keys}), encoding="utf-8")
    subprocess.run(["python3", str(root / "scripts" / "montar_relatorio.py"), "--data", str(data), "--out", str(output)], check=True)
    html = output.read_text(encoding="utf-8")
    assert "{{" not in html
    assert "<style>" in html and "report.css" not in html
    forbidden = ["Money" + "Brand", "doug" + "demarco"]
    assert all(term.lower() not in html.lower() for term in forbidden)
print("HTML autonomo passou: sem marcador, folha externa ou assinatura de terceiro")
