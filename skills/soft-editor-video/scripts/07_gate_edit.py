#!/usr/bin/env python3
"""Gate mecânico da timeline antes do export e da auditoria final."""
import json
import os
import sys
import tempfile


def _number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def validate(data, check_files=True):
    errors = []
    mode = data.get("layout_mode")
    adaptive = mode == "adaptive"
    if mode not in {"adaptive", "fullscreen-proof", "top-fixed", "feed-plain"}:
        errors.append("layout_mode invalido")
    if adaptive:
        if data.get("caption_mode") != "word":
            errors.append("legenda precisa ser palavra por palavra")
        if data.get("keyword_highlight") is not True:
            errors.append("falta destaque da palavra-chave")
        ratio = data.get("layout_flip_ratio")
        if not _number(ratio) or not 0.20 <= ratio <= 0.45:
            errors.append("virada de layout precisa ficar entre 20% e 45%")
    if data.get("speech_speed") not in (1, 1.0, 1.2):
        errors.append("velocidade fora das familias aprovadas")

    words = data.get("speech_words")
    if not isinstance(words, list) or not words:
        errors.append("fala compactada sem palavras e tempos")
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
    if not isinstance(compaction, dict) or compaction.get("word_timed") is not True:
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
    for index, segment in enumerate(segments, 1):
        try:
            duration = float(segment["end"]) - float(segment["start"])
        except (KeyError, TypeError, ValueError):
            errors.append(f"apoio {index} sem tempo valido")
            continue
        if duration <= 0:
            errors.append(f"apoio {index} tem duracao invalida")
        if duration > 3.4 and segment.get("type") != "real_screen" and not segment.get("exception"):
            errors.append(f"apoio {index} dura {duration:.2f}s sem excecao")
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
        "support_segments": [{"start": 0, "end": 2.7, "type": "image"}],
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
        return all(validate(variant) for variant in variants)


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
