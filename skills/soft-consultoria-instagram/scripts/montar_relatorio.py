#!/usr/bin/env python3
"""Monta um HTML autônomo da consultoria de Instagram."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    skill = Path(__file__).resolve().parent.parent
    template = (skill / "assets" / "report-template.html").read_text(encoding="utf-8")
    css = (skill / "assets" / "report.css").read_text(encoding="utf-8")
    data = json.loads(Path(args.data).read_text(encoding="utf-8"))
    required = {
        "CLIENT", "DATE", "HERO_RESULT", "TWO_MINUTE_SUMMARY", "VISITOR_JOURNEY",
        "CENTRAL_DIAGNOSIS", "CURRENT_TO_FUTURE_SYSTEM", "FOUR_PROFILE_JOBS",
        "READY_TO_BUILD_SYSTEM", "EXECUTION_AND_FUTURE_STATE", "TECHNICAL_APPENDIX"
    }
    missing = sorted(required - set(data))
    if missing:
        raise SystemExit(f"ERRO: campos ausentes: {', '.join(missing)}")
    html = template.replace("{{INLINE_CSS}}", css)
    for key in required:
        html = html.replace("{{" + key + "}}", str(data[key]))
    markers = sorted(set(re.findall(r"\{\{[A-Z0-9_]+\}\}", html)))
    if markers:
        raise SystemExit(f"ERRO: marcadores abertos: {', '.join(markers)}")
    Path(args.out).write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
