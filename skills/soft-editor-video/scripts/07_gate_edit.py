#!/usr/bin/env python3
"""Gate mecânico da timeline antes do export e da auditoria final."""
import json
import os
import sys
import tempfile


def _number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def validate(data, check_files=True):
    errors = []
    # Insumo sem fala e caminho previsto, nao falha: speech_words vazio + motivo
    # medido em no_speech_reason libera os criterios que dependem de fala
    # (legenda palavra por palavra, tempos e compactacao). Texto falso dentro de
    # speech_words so pra satisfazer o formato continua reprovando.
    raw_words = data.get("speech_words")
    no_speech_reason = data.get("no_speech_reason")
    no_speech = isinstance(raw_words, list) and not raw_words and _text(no_speech_reason)
    if isinstance(raw_words, list):
        for item in raw_words:
            word = str(item.get("word", "")).strip() if isinstance(item, dict) else str(item).strip()
            if word.startswith("[") and word.endswith("]"):
                errors.append("speech_words com marcador no lugar de fala real")
                break
    mode = data.get("layout_mode")
    adaptive = mode == "adaptive"
    if mode not in {"adaptive", "fullscreen-proof", "top-fixed", "feed-plain"}:
        errors.append("layout_mode invalido")
    if adaptive and not no_speech:
        if data.get("caption_mode") != "word":
            errors.append("legenda precisa ser palavra por palavra")
        if data.get("keyword_highlight") is not True:
            errors.append("falta destaque da palavra-chave")
        ratio = data.get("layout_flip_ratio")
        if not _number(ratio) or not 0.20 <= ratio <= 0.45:
            errors.append("virada de layout precisa ficar entre 20% e 45%")
    if data.get("speech_speed") not in (1, 1.0, 1.2):
        errors.append("velocidade fora das familias aprovadas")

    words = raw_words
    if no_speech:
        pass
    elif not isinstance(words, list) or not words:
        errors.append("fala compactada sem palavras e tempos (sem fala no material: grave speech_words: [] e no_speech_reason com o motivo medido)")
    else:
        previous_start = -1.0
        for index, item in enumerate(words, 1):
            if not isinstance(item, dict) or not str(item.get("word", "")).strip():
                errors.append(f"palavra {index} sem texto")
                continue
            start, end = item.get("start"), item.get("end")
            if not _number(start) or not _number(end) or start < 0 or end <= start:
                errors.append(f"palavra {index} sem tempo valido")
            elif start < previous_start:
                errors.append(f"palavra {index} fora de ordem")
            else:
                previous_start = start

    compaction = data.get("speech_compaction")
    if no_speech:
        pass
    elif not isinstance(compaction, dict) or compaction.get("word_timed") is not True:
        errors.append("fala compactada sem prova word-timed")
    else:
        source_duration = compaction.get("source_duration")
        timeline_duration = compaction.get("timeline_duration")
        if (not _number(source_duration) or not _number(timeline_duration)
                or source_duration <= 0 or timeline_duration <= 0
                or timeline_duration > source_duration + 0.05):
            errors.append("duracoes da fala compactada invalidas")

    cuts = data.get("cut_map")
    cut_ids = []
    if not isinstance(cuts, list) or not cuts:
        errors.append("mapa explicito de cortes ausente")
    else:
        previous_source_start = -1.0
        previous_timeline_end = 0.0
        seen_ids = set()
        for index, cut in enumerate(cuts, 1):
            cut_id = cut.get("id") if isinstance(cut, dict) else None
            if not cut_id or cut_id in seen_ids:
                errors.append(f"corte {index} sem id unico")
                continue
            seen_ids.add(cut_id)
            cut_ids.append(cut_id)
            fields = [cut.get(name) for name in (
                "source_start", "source_end", "timeline_start", "timeline_end"
            )]
            if not all(_number(value) for value in fields):
                errors.append(f"corte {cut_id} sem tempos validos")
                continue
            source_start, source_end, timeline_start, timeline_end = fields
            if source_start < 0 or source_end <= source_start:
                errors.append(f"corte {cut_id} com origem invalida")
            if timeline_start < 0 or timeline_end <= timeline_start:
                errors.append(f"corte {cut_id} com destino invalido")
            if source_start < previous_source_start:
                errors.append(f"corte {cut_id} fora da ordem da fonte")
            if abs(timeline_start - previous_timeline_end) > 0.05:
                errors.append(f"corte {cut_id} deixa lacuna na timeline")
            previous_source_start = source_start
            previous_timeline_end = timeline_end
            if cut.get("audio_fade_in_ms") != 30 or cut.get("audio_fade_out_ms") != 30:
                errors.append(f"corte {cut_id} sem fades de audio de 30 ms")

    order = data.get("render_order")
    if not isinstance(order, list):
        errors.append("ordem de render ausente")
    elif "animations_overlays" not in order or "captions" not in order:
        errors.append("ordem precisa declarar animacoes/overlays e legenda")
    elif order.index("captions") <= order.index("animations_overlays"):
        errors.append("legenda precisa ser aplicada depois das animacoes/overlays")

    inspections = data.get("cut_inspections")
    if not isinstance(inspections, list):
        errors.append("inspecao visual dos cortes ausente")
    else:
        indexed = {
            item.get("cut_id"): item for item in inspections
            if isinstance(item, dict) and item.get("cut_id")
        }
        for cut_id in cut_ids[1:]:
            item = indexed.get(cut_id)
            if not item or item.get("passed") is not True:
                errors.append(f"corte {cut_id} sem inspecao visual aprovada")
                continue
            proof = item.get("proof")
            if not isinstance(proof, str) or not os.path.isabs(proof):
                errors.append(f"corte {cut_id} sem prova visual absoluta")
            elif check_files and not os.path.isfile(proof):
                errors.append(f"corte {cut_id} com prova visual inexistente")
            if item.get("reviewer") != "codex-oauth":
                errors.append(f"corte {cut_id} sem visao da conta ChatGPT")

    paid = data.get("paid_generation", {})
    if paid.get("provider", "none") != "none" and paid.get("approved") is not True:
        errors.append("geracao com creditos sem aprovacao registrada")
    segments = data.get("support_segments", [])
    if adaptive and not segments:
        errors.append("composicao adaptativa sem apoios")
    if segments:
        direction = data.get("visual_direction")
        if not isinstance(direction, dict):
            errors.append("direcao visual central ausente")
        else:
            for field in ("semantic_division", "continuity_rule", "phrase_rhythm",
                          "transition_language"):
                if not _text(direction.get(field)):
                    errors.append(f"direcao visual sem {field}")
            if direction.get("director_reviewed") is not True:
                errors.append("direcao visual sem revisao central")
    for index, segment in enumerate(segments, 1):
        if not isinstance(segment, dict):
            errors.append(f"apoio {index} invalido")
            continue
        try:
            duration = float(segment["end"]) - float(segment["start"])
        except (KeyError, TypeError, ValueError):
            errors.append(f"apoio {index} sem tempo valido")
            continue
        if duration <= 0:
            errors.append(f"apoio {index} tem duracao invalida")
        if duration > 3.4 and segment.get("type") != "real_screen" and not segment.get("exception"):
            errors.append(f"apoio {index} dura {duration:.2f}s sem excecao")
        for field in ("speech_excerpt", "intent", "visual_strategy", "first_frame_plan",
                      "last_frame_plan", "motion", "transition_in", "transition_out"):
            if not _text(segment.get(field)):
                errors.append(f"apoio {index} sem {field}")
        phrase = segment.get("support_phrase")
        if not isinstance(phrase, dict):
            errors.append(f"apoio {index} sem decisao de frase")
        elif phrase.get("decision") == "use":
            if not _text(phrase.get("text")) or not _text(phrase.get("role")):
                errors.append(f"apoio {index} com frase incompleta")
        elif phrase.get("decision") == "none":
            if not _text(phrase.get("reason")):
                errors.append(f"apoio {index} sem motivo para nao usar frase")
        else:
            errors.append(f"apoio {index} com decisao de frase invalida")
    reveals = data.get("list_reveals", [])
    if len(reveals) > 1:
        times = [item.get("at") for item in reveals]
        if any(not _number(value) for value in times) or len(set(times)) != len(times):
            errors.append("itens da lista nao entram um por vez")
    final = data.get("final")
    if final and not os.path.isabs(final):
        errors.append("caminho final precisa ser absoluto")
    return errors


def sample_manifest(proof):
    return {
        "layout_mode": "adaptive",
        "caption_mode": "word",
        "keyword_highlight": True,
        "layout_flip_ratio": 0.31,
        "speech_speed": 1.2,
        "speech_words": [
            {"word": "fala", "start": 0.0, "end": 0.3},
            {"word": "limpa", "start": 0.32, "end": 0.7},
        ],
        "speech_compaction": {
            "source_duration": 3.0, "timeline_duration": 2.0,
            "removed_duration": 1.0, "word_timed": True,
        },
        "cut_map": [
            {"id": "cut-001", "source_start": 0.0, "source_end": 1.0,
             "timeline_start": 0.0, "timeline_end": 1.0,
             "audio_fade_in_ms": 30, "audio_fade_out_ms": 30},
            {"id": "cut-002", "source_start": 2.0, "source_end": 3.0,
             "timeline_start": 1.0, "timeline_end": 2.0,
             "audio_fade_in_ms": 30, "audio_fade_out_ms": 30},
        ],
        "render_order": ["base", "animations_overlays", "captions", "music"],
        "cut_inspections": [
            {"cut_id": "cut-002", "passed": True, "proof": proof,
             "reviewer": "codex-oauth"}
        ],
        "visual_direction": {
            "semantic_division": "blocos de argumento",
            "continuity_rule": "uma linguagem visual",
            "phrase_rhythm": "frases apenas nas ideias fortes",
            "transition_language": "transicoes motivadas pela fala",
            "director_reviewed": True,
        },
        "support_segments": [{
            "start": 0, "end": 2.7, "type": "image",
            "speech_excerpt": "fala limpa", "intent": "mostrar a acao",
            "visual_strategy": "a ordem vira resultado",
            "support_phrase": {"decision": "use", "text": "Ordem em trabalho",
                               "role": "tese"},
            "first_frame_plan": "ordem no celular",
            "last_frame_plan": "resultado na tela",
            "motion": "onda de audio vira resultado",
            "transition_in": "camera entra no celular",
            "transition_out": "resultado ocupa o quadro",
        }],
        "list_reveals": [{"at": 2.0}, {"at": 3.0}],
        "paid_generation": {"provider": "none", "credits": 0, "approved": True},
    }


def self_test():
    with tempfile.TemporaryDirectory() as directory:
        proof = os.path.join(directory, "cut-002.jpg")
        with open(proof, "wb") as handle:
            handle.write(b"proof")
        good = sample_manifest(proof)
        if validate(good) != []:
            return False
        variants = []
        for missing in ("speech_words", "cut_map", "render_order", "cut_inspections"):
            variant = dict(good)
            variant.pop(missing)
            variants.append(variant)
        no_fade = json.loads(json.dumps(good))
        no_fade["cut_map"][1].pop("audio_fade_in_ms")
        variants.append(no_fade)
        wrong_order = dict(good, render_order=["base", "captions", "animations_overlays"])
        variants.append(wrong_order)
        no_direction = json.loads(json.dumps(good))
        no_direction.pop("visual_direction")
        variants.append(no_direction)
        no_phrase = json.loads(json.dumps(good))
        no_phrase["support_segments"][0].pop("support_phrase")
        variants.append(no_phrase)
        no_transition = json.loads(json.dumps(good))
        no_transition["support_segments"][0].pop("transition_out")
        variants.append(no_transition)
        # sem fala mas sem motivo medido: continua reprovando
        empty_no_reason = json.loads(json.dumps(good))
        empty_no_reason["speech_words"] = []
        variants.append(empty_no_reason)
        # marcador falso no lugar de fala real: reprova
        fake_word = json.loads(json.dumps(good))
        fake_word["speech_words"] = [{"word": "[sem_fala_no_material]", "start": 0, "end": 1}]
        variants.append(fake_word)
        if not all(validate(variant) for variant in variants):
            return False
        # caminho previsto: sem fala, com motivo medido, o gate ACEITA
        no_speech = json.loads(json.dumps(good))
        no_speech["speech_words"] = []
        no_speech["no_speech_reason"] = "material sem fala: medido na ingestao"
        no_speech.pop("speech_compaction", None)
        return validate(no_speech) == []


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv == ["--self-test"]:
        if self_test():
            print("PASSA: self-test")
            return 0
        print("FALHA: self-test")
        return 1
    if len(argv) != 1:
        print("uso: 07_gate_edit.py edit-manifest.json")
        return 2
    with open(argv[0], encoding="utf-8") as handle:
        manifest = json.load(handle)
    problems = validate(manifest)
    if problems:
        print("FALHA: " + " | ".join(problems))
        return 1
    print("PASSA: timeline dentro da regua")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
