#!/usr/bin/env python3
"""Calcula a nota de sistema comercial a partir de audit-score.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path


WEIGHTS = {
    "posicionamento": 12,
    "mecanismo": 14,
    "narrativa": 12,
    "repeticao": 8,
    "arquitetura_editorial": 10,
    "prova": 8,
    "funil": 12,
    "bio_link_oferta": 10,
    "encarnacao": 8,
    "perfil_sistema": 6,
}

SOURCE_WEIGHTS = {
    "profile_surface": 15,
    "posts_sample": 25,
    "carousels": 15,
    "reels": 20,
    "highlights": 10,
    "link_destination": 15,
}

SOURCE_FACTORS = {
    "verified": 1.0,
    "partial": 0.5,
    "not_accessed": 0.0,
    "not_applicable": None,
}

EVIDENCE_CLASSES = {"observado", "declarado", "inferido", "hipotese", "nao_determinavel_externamente"}


def validate_evidence(dim_id: str, evidence: object, quality: int) -> list[dict]:
    if not isinstance(evidence, list) or not evidence:
        fail(f"{dim_id}: dimensao pontuada exige evidence nao vazia")
    checked = []
    for index, item in enumerate(evidence, start=1):
        if not isinstance(item, dict):
            fail(f"{dim_id}: evidencia {index} deve ser objeto com text, source e class")
        text = str(item.get("text", "")).strip()
        source = str(item.get("source", "")).strip()
        evidence_class = item.get("class")
        if not text or not source or evidence_class not in EVIDENCE_CLASSES:
            fail(f"{dim_id}: evidencia {index} incompleta ou com class invalida")
        checked.append(item)
    minimum = 1 if quality == 1 else 2
    if len(checked) < minimum:
        fail(f"{dim_id}: evidence_quality {quality} exige ao menos {minimum} evidencias")
    if quality == 3 and len({str(item['source']).strip() for item in checked}) < 2:
        fail(f"{dim_id}: evidence_quality 3 exige duas fontes identificadas")
    return checked


def band(score: float) -> str:
    if score >= 90:
        return "Sistema comercial integrado"
    if score >= 80:
        return "Marca comercial forte"
    if score >= 70:
        return "Posicionamento funcional com lacunas"
    if score >= 55:
        return "Sistema incompleto"
    if score >= 40:
        return "Conteudo sem arquitetura comercial suficiente"
    return "Perfil fragmentado ou proposta ilegivel"


def fail(message: str) -> None:
    raise SystemExit(f"ERRO: {message}")


def main() -> None:
    if len(sys.argv) != 2:
        fail("uso: calcular_pontuacao.py audit-score.json")

    path = Path(sys.argv[1])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"arquivo nao encontrado: {path}")
    except json.JSONDecodeError as exc:
        fail(f"JSON invalido: {exc}")

    rows = data.get("dimensions")
    if not isinstance(rows, list):
        fail("dimensions deve ser uma lista")

    source_rows = data.get("source_coverage")
    if not isinstance(source_rows, list):
        fail("source_coverage deve ser uma lista")

    source_by_id = {}
    for row in source_rows:
        if not isinstance(row, dict) or "id" not in row:
            fail("cada item de source_coverage precisa de id")
        source_id = row["id"]
        if source_id in source_by_id:
            fail(f"source_coverage com id duplicado: {source_id}")
        source_by_id[source_id] = row

    missing_sources = sorted(set(SOURCE_WEIGHTS) - set(source_by_id))
    extra_sources = sorted(set(source_by_id) - set(SOURCE_WEIGHTS))
    if missing_sources:
        fail(f"fontes ausentes: {', '.join(missing_sources)}")
    if extra_sources:
        fail(f"fontes desconhecidas: {', '.join(extra_sources)}")

    applicable_source_weight = 0
    verified_source_points = 0.0
    source_details = []
    for source_id, weight in SOURCE_WEIGHTS.items():
        status = source_by_id[source_id].get("status")
        if status not in SOURCE_FACTORS:
            fail(
                f"{source_id}: status deve ser verified, partial, "
                "not_accessed ou not_applicable"
            )
        factor = SOURCE_FACTORS[status]
        if factor is not None:
            applicable_source_weight += weight
            verified_source_points += factor * weight
        source_details.append(
            {
                "id": source_id,
                "weight": weight,
                "status": status,
                "note": source_by_id[source_id].get("note"),
            }
        )

    if applicable_source_weight == 0:
        fail("nenhuma superficie de fonte foi considerada aplicavel")

    by_id = {}
    for row in rows:
        if not isinstance(row, dict) or "id" not in row:
            fail("cada dimensao precisa de id")
        dim_id = row["id"]
        if dim_id in by_id:
            fail(f"id duplicado: {dim_id}")
        by_id[dim_id] = row

    missing = sorted(set(WEIGHTS) - set(by_id))
    extra = sorted(set(by_id) - set(WEIGHTS))
    if missing:
        fail(f"dimensoes ausentes: {', '.join(missing)}")
    if extra:
        fail(f"dimensoes desconhecidas: {', '.join(extra)}")

    evaluated_weight = 0
    earned_points = 0.0
    confidence_points = 0.0
    details = []

    for dim_id, weight in WEIGHTS.items():
        row = by_id[dim_id]
        score = row.get("score")
        evidence_quality = row.get("evidence_quality", 0)
        evidence = row.get("evidence")

        if not isinstance(evidence_quality, int) or not 0 <= evidence_quality <= 3:
            fail(f"{dim_id}: evidence_quality deve ser inteiro entre 0 e 3")

        if score is None:
            if evidence_quality != 0:
                fail(f"{dim_id}: score null exige evidence_quality 0")
            if not isinstance(evidence, list) or not any(str(item).strip() for item in evidence):
                fail(f"{dim_id}: score null exige explicacao em evidence")
            details.append({"id": dim_id, "weight": weight, "score": None, "points": None})
            continue

        if not isinstance(score, (int, float)) or isinstance(score, bool) or not 0 <= score <= 5:
            fail(f"{dim_id}: score deve estar entre 0 e 5 ou ser null")
        if evidence_quality == 0:
            fail(f"{dim_id}: dimensao pontuada exige evidence_quality maior que 0")
        validate_evidence(dim_id, evidence, evidence_quality)

        points = score / 5 * weight
        evaluated_weight += weight
        earned_points += points
        confidence_points += evidence_quality / 3 * weight
        details.append(
            {
                "id": dim_id,
                "weight": weight,
                "score": score,
                "points": round(points, 2),
            }
        )

    if evaluated_weight == 0:
        fail("nenhuma dimensao foi avaliada")

    normalized = earned_points / evaluated_weight * 100
    dimension_coverage = evaluated_weight
    source_coverage = verified_source_points / applicable_source_weight * 100
    coverage = min(dimension_coverage, source_coverage)
    raw_confidence = confidence_points / evaluated_weight * 100
    confidence = min(raw_confidence, source_coverage)

    ceiling = 100
    ceiling_reasons = []

    pos = by_id["posicionamento"].get("score")
    mech = by_id["mecanismo"].get("score")
    if pos is not None and mech is not None and (pos <= 1 or mech <= 1):
        ceiling = min(ceiling, 59)
        ceiling_reasons.append("posicionamento ou mecanismo sem espinha funcional")

    funnel = by_id["funil"].get("score")
    bio = by_id["bio_link_oferta"].get("score")
    if funnel is not None and bio is not None and funnel <= 1 and bio <= 1:
        ceiling = min(ceiling, 69)
        ceiling_reasons.append("funil e bio/link/oferta sem continuidade")

    final_score = min(normalized, ceiling)
    status = "definitivo" if coverage >= 70 and confidence >= 70 else "provisorio"

    # Gate de nota invalida: cobertura abaixo do minimo com todas as dimensoes
    # pontuadas significa que a falta de prova virou nota, e nao `score: null`.
    # Nesse caso a nota final NAO sai; sai o motivo e a lista do que coletar.
    scored_ids = [row["id"] for row in details if row["score"] is not None]
    null_ids = [row["id"] for row in details if row["score"] is None]
    invalid_reasons = []
    if coverage < 70 and dimension_coverage >= 100:
        invalid_reasons.append(
            f"cobertura de {round(coverage, 1)}% abaixo do minimo de 70% com as "
            f"{len(scored_ids)} dimensoes pontuadas e nenhuma em score null: "
            "dimensao sem prova precisa sair como score null e evidence_quality 0"
        )
    if confidence < 70 and not null_ids and all(
        by_id[dim].get("evidence_quality") == 1 for dim in scored_ids
    ):
        invalid_reasons.append(
            f"confianca de {round(confidence, 1)}% com evidence_quality 1 uniforme "
            "em todas as dimensoes: evidencia fraca uniforme nao sustenta nota final"
        )
    for dim_id in scored_ids:
        classes = {
            str(item.get("class", "")).strip()
            for item in by_id[dim_id].get("evidence", [])
            if isinstance(item, dict)
        }
        if classes and classes <= {"nao_determinavel_externamente"}:
            invalid_reasons.append(
                f"{dim_id}: dimensao pontuada apoiada so em evidencia "
                "nao_determinavel_externamente; use score null"
            )

    if invalid_reasons:
        blocked = {
            "profile": data.get("profile"),
            "audited_at": data.get("audited_at"),
            "score": None,
            "band": None,
            "status": "nota_invalida",
            "invalid_reasons": invalid_reasons,
            "dimension_coverage_percent": round(dimension_coverage, 1),
            "source_coverage_percent": round(source_coverage, 1),
            "coverage_percent": round(coverage, 1),
            "confidence_percent": round(confidence, 1),
            "missing_sources": [
                row["id"]
                for row in source_details
                if row["status"] in {"not_accessed", "partial"}
            ],
            "source_coverage": source_details,
            "dimensions": details,
        }
        print(json.dumps(blocked, ensure_ascii=False, indent=2))
        raise SystemExit(
            "ERRO: nota invalida, sem numero final. "
            + " | ".join(invalid_reasons)
        )

    result = {
        "profile": data.get("profile"),
        "audited_at": data.get("audited_at"),
        "score": round(final_score, 1),
        "score_before_ceiling": round(normalized, 1),
        "band": band(final_score),
        "dimension_coverage_percent": round(dimension_coverage, 1),
        "source_coverage_percent": round(source_coverage, 1),
        "coverage_percent": round(coverage, 1),
        "confidence_percent": round(confidence, 1),
        "status": status,
        "commercial_ceiling": ceiling,
        "ceiling_reasons": ceiling_reasons,
        "source_coverage": source_details,
        "dimensions": details,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
