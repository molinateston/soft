#!/usr/bin/env python3
"""Gate mecânico para o mapa visual integrado, antes de gerar qualquer apoio."""
import copy
import json
import sys


def _number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def validate(plan):
    """Return all mechanical problems found in a visual-plan manifest.

    Expected top-level fields are ``recorte``, ``semantic_blocks``,
    ``visual_direction``, ``central_review``, ``decisions`` and
    ``cost_total_brl``. Times are expressed in seconds.
    """
    errors = []
    # Insumo mais curto que o recorte minimo e caminho previsto, nao falha:
    # com short_input_reason preenchido (a duracao medida), o gate pula os
    # criterios de recorte e de blocos semanticos e cobra so o que se aplica.
    short_reason = plan.get("short_input_reason") if isinstance(plan, dict) else None
    short_input = bool(_text(short_reason))
    recorte = plan.get("recorte") if isinstance(plan, dict) else None
    if not isinstance(recorte, dict):
        if not short_input:
            errors.append("recorte ausente")
        clip_start = clip_end = None
    else:
        clip_start, clip_end = recorte.get("start"), recorte.get("end")
        if (not _number(clip_start) or not _number(clip_end)
                or clip_start < 0 or clip_end <= clip_start):
            errors.append("recorte precisa ter start e end validos")
        elif not short_input and not 60 <= clip_end - clip_start <= 90:
            errors.append("recorte precisa durar entre 60 e 90 segundos")

    blocks = plan.get("semantic_blocks") if isinstance(plan, dict) else None
    block_ids = set()
    if not isinstance(blocks, list) or len(blocks) < (1 if short_input else 2):
        errors.append("e exigido pelo menos um bloco semantico"
                      if short_input else "sao exigidos dois ou mais blocos semanticos")
    else:
        for index, block in enumerate(blocks, 1):
            if not isinstance(block, dict):
                errors.append(f"bloco {index} invalido")
                continue
            block_id = block.get("id")
            if not _text(block_id) or block_id in block_ids:
                errors.append(f"bloco {index} sem id unico")
            else:
                block_ids.add(block_id)
            for field in ("context_before", "context_after", "exact_speech"):
                if not _text(block.get(field)):
                    errors.append(f"bloco {index} sem {field}")
            if block.get("independent_review") is not True:
                errors.append(f"bloco {index} sem revisao independente")

    direction = plan.get("visual_direction") if isinstance(plan, dict) else None
    if not isinstance(direction, dict):
        errors.append("direcao visual central ausente")
    else:
        for field in ("semantic_division", "continuity_rule", "phrase_rhythm",
                      "transition_language"):
            if not _text(direction.get(field)):
                errors.append(f"direcao visual sem {field}")

    review = plan.get("central_review") if isinstance(plan, dict) else None
    if not isinstance(review, dict) or review.get("reviewed") is not True:
        errors.append("revisao central verdadeira ausente")
    else:
        for field in ("repetition_removed", "language_unified", "proof_preserved"):
            if field not in review:
                errors.append(f"revisao central sem {field}")

    decisions = plan.get("decisions") if isinstance(plan, dict) else None
    costs = []
    # A cota de 8 a 12 decisoes pressupoe um recorte de 60 a 90s. Com
    # short_input_reason preenchido o recorte e menor por medicao, entao a cota
    # cai pro piso de 1: cobrar 8 decisoes de um bruto que nao as comporta
    # so premia quem inventa decisao pra passar no gate.
    minimo = 1 if short_input else 8
    if not isinstance(decisions, list) or not minimo <= len(decisions) <= 12:
        errors.append(f"sao exigidas entre {minimo} e 12 decisoes")
    else:
        seen_ids = set()
        previous_end = None
        for index, decision in enumerate(decisions, 1):
            if not isinstance(decision, dict):
                errors.append(f"decisao {index} invalida")
                continue
            decision_id = decision.get("id")
            if not _text(decision_id) or decision_id in seen_ids:
                errors.append(f"decisao {index} sem id unico")
            else:
                seen_ids.add(decision_id)
            if decision.get("block") not in block_ids:
                errors.append(f"decisao {index} com bloco invalido")
            start, end = decision.get("start"), decision.get("end")
            if (not _number(start) or not _number(end) or end <= start
                    or (_number(clip_start) and start < clip_start)
                    or (_number(clip_end) and end > clip_end)):
                errors.append(f"decisao {index} sem tempos validos no recorte")
            elif previous_end is not None and start < previous_end:
                errors.append(f"decisao {index} fora da ordem temporal")
            if _number(end):
                previous_end = end
            for field in ("literal_speech", "intent", "support_type", "visual_strategy",
                          "first_frame", "last_frame", "motion", "transition_in",
                          "transition_out", "reusable_material"):
                if not _text(decision.get(field)):
                    errors.append(f"decisao {index} sem {field}")
            phrase = decision.get("support_phrase")
            if not isinstance(phrase, dict):
                errors.append(f"decisao {index} sem decisao de frase")
            elif phrase.get("decision") == "use":
                for field in ("text", "role", "editorial_reason"):
                    if not _text(phrase.get(field)):
                        errors.append(f"decisao {index} com frase sem {field}")
            elif phrase.get("decision") == "none":
                if not _text(phrase.get("reason")):
                    errors.append(f"decisao {index} sem reason para nao usar frase")
            else:
                errors.append(f"decisao {index} com decisao de frase invalida")
            cost = decision.get("cost_brl")
            if not _number(cost) or cost < 0:
                errors.append(f"decisao {index} sem custo previsto valido")
            else:
                costs.append(cost)

    total = plan.get("cost_total_brl") if isinstance(plan, dict) else None
    if not _number(total):
        errors.append("cost_total_brl invalido")
    elif len(costs) == (len(decisions) if isinstance(decisions, list) else 0):
        if abs(total - sum(costs)) > 1e-6:
            errors.append("cost_total_brl difere da soma das decisoes")
    return errors


def sample_plan():
    blocks = [
        {"id": "diagnostico", "context_before": "abertura", "context_after": "mecanismo",
         "exact_speech": "O problema tem um padrao claro.", "independent_review": True},
        {"id": "mecanismo", "context_before": "diagnostico", "context_after": "prova",
         "exact_speech": "Agora veja como a mudanca acontece.", "independent_review": True},
    ]
    decisions = []
    for index in range(8):
        start = index * 8
        decisions.append({
            "id": f"dec-{index + 1:02d}", "block": blocks[index % 2]["id"],
            "start": start, "end": start + 7, "literal_speech": "Fala literal do trecho.",
            "intent": "explicar o argumento", "support_type": "prova real",
            "visual_strategy": "demonstracao progressiva", "support_phrase": {
                "decision": "use", "text": "Ideia principal", "role": "tese",
                "editorial_reason": "fixa a conclusao sem repetir a legenda"},
            "first_frame": "prova em tela", "last_frame": "resultado confirmado",
            "motion": "resultado avanca", "transition_in": "tela ocupa o quadro",
            "transition_out": "resultado abre o proximo argumento",
            "reusable_material": "captura de tela existente", "cost_brl": 0,
        })
    return {
        "recorte": {"start": 0, "end": 64}, "semantic_blocks": blocks,
        "visual_direction": {"semantic_division": "diagnostico e mecanismo",
                             "continuity_rule": "prova limpa em tela",
                             "phrase_rhythm": "uma tese por virada",
                             "transition_language": "transicoes motivadas pela fala"},
        "central_review": {"reviewed": True, "repetition_removed": True,
                           "language_unified": True, "proof_preserved": True},
        "decisions": decisions, "cost_total_brl": 0,
    }


def self_test():
    good = sample_plan()
    if validate(good):
        return False
    for path in (("decisions", 0, "support_phrase"), ("decisions", 0, "first_frame"),
                 ("decisions", 0, "transition_out"), ("decisions", 0, "start"),
                 ("decisions", 0, "literal_speech"), ("central_review",)):
        broken = copy.deepcopy(good)
        target = broken
        for key in path[:-1]:
            target = target[key]
        target.pop(path[-1])
        if not validate(broken):
            return False
    return True


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv == ["--self-test"]:
        print("PASSA: self-test" if self_test() else "FALHA: self-test")
        return 0 if self_test() else 1
    if len(argv) != 1:
        print("uso: 08_gate_visual_plan.py visual-plan.json")
        return 2
    try:
        with open(argv[0], encoding="utf-8") as handle:
            plan = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FALHA: {exc}")
        return 1
    errors = validate(plan)
    if errors:
        print("FALHA: " + " | ".join(errors))
        return 1
    print("PASSA: mapa visual dentro da regua")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
