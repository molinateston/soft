#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).with_name("calcular_pontuacao.py")
DIMENSIONS = ["posicionamento", "mecanismo", "narrativa", "repeticao", "arquitetura_editorial", "prova", "funil", "bio_link_oferta", "encarnacao", "perfil_sistema"]
SOURCES = ["profile_surface", "posts_sample", "carousels", "reels", "highlights", "link_destination"]


def run(payload: dict) -> subprocess.CompletedProcess[str]:
    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as handle:
        json.dump(payload, handle)
        path = handle.name
    return subprocess.run(["python3", str(SCRIPT), path], text=True, capture_output=True)


def payload(score: float | None, quality: int, evidence: list[dict] | list[str], source_status: str) -> dict:
    return {
        "profile": "@teste",
        "audited_at": "2026-08-31T17:25:00-03:00",
        "source_coverage": [{"id": source, "status": source_status, "note": "teste"} for source in SOURCES],
        "dimensions": [{"id": dimension, "score": score, "evidence_quality": quality, "evidence": evidence} for dimension in DIMENSIONS],
    }


empty = run(payload(5, 3, [], "verified"))
assert empty.returncode != 0 and "evidence nao vazia" in empty.stderr + empty.stdout

partial_evidence = [{"text": "bio observada", "source": "perfil", "class": "observado"}]

# Cobertura abaixo do minimo com TODAS as dimensoes pontuadas: nota invalida,
# sem numero final. Falta de prova precisa virar score null, nunca nota baixa.
partial = run(payload(3, 1, partial_evidence, "partial"))
assert partial.returncode != 0, "cobertura baixa com tudo pontuado tem que recusar"
blocked = json.loads(partial.stdout)
assert blocked["score"] is None and blocked["status"] == "nota_invalida"
assert blocked["coverage_percent"] < 70

# O mesmo caso, feito direito: as dimensoes sem prova saem com score null.
# A nota sai, marcada provisoria.
honest = payload(3, 1, partial_evidence, "partial")
for row in honest["dimensions"][:4]:
    row["score"] = None
    row["evidence_quality"] = 0
    row["evidence"] = ["sem prova coletada nesta superficie"]
honest_run = run(honest)
assert honest_run.returncode == 0, honest_run.stderr
assert json.loads(honest_run.stdout)["status"] == "provisorio"

# Dimensao pontuada apoiada so em evidencia nao determinavel externamente.
indeterminada = payload(4, 3, [
    {"text": "bio observada", "source": "perfil", "class": "observado"},
    {"text": "tese repetida", "source": "post-1", "class": "observado"},
], "verified")
for row in indeterminada["dimensions"]:
    if row["id"] == "encarnacao":
        row["score"] = 1
        row["evidence_quality"] = 1
        row["evidence"] = [{"text": "nao da pra ver de fora", "source": "perfil", "class": "nao_determinavel_externamente"}]
indeterminada_run = run(indeterminada)
assert indeterminada_run.returncode != 0, "nota apoiada so em indeterminavel tem que recusar"
assert "nao_determinavel_externamente" in indeterminada_run.stderr

sufficient_evidence = [
    {"text": "bio observada", "source": "perfil", "class": "observado"},
    {"text": "tese repetida", "source": "post-1", "class": "observado"},
]
sufficient = run(payload(4, 3, sufficient_evidence, "verified"))
assert sufficient.returncode == 0
result = json.loads(sufficient.stdout)
assert result["status"] == "definitivo" and result["confidence_percent"] == 100.0

print("5 cenarios passaram: vazio recusado, cobertura baixa com tudo pontuado recusada, null honesto provisorio, indeterminavel recusado, suficiente definitivo")
