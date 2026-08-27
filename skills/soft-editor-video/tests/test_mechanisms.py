#!/usr/bin/env python3
import copy
import importlib.util
import os
import tempfile
import unittest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_module(name, relative_path):
    path = os.path.join(ROOT, relative_path)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


gate = load_module("gate_edit", "scripts/07_gate_edit.py")
silence = load_module("silence_cut", "scripts/00_silence_cut.py")
inspection = load_module("inspect_cuts", "scripts/06_inspect_cuts.py")


class MechanismBenchTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.proof = os.path.join(self.temp.name, "mosaico.jpg")
        with open(self.proof, "wb") as handle:
            handle.write(b"proof")
        self.good = gate.sample_manifest(self.proof)

    def tearDown(self):
        self.temp.cleanup()

    def assert_reproves(self, manifest, fragment):
        errors = gate.validate(manifest)
        self.assertTrue(any(fragment in error for error in errors), errors)

    def test_complete_manifest_passes(self):
        self.assertEqual([], gate.validate(self.good))

    def test_missing_word_timing_reproves(self):
        manifest = copy.deepcopy(self.good)
        manifest.pop("speech_words")
        self.assert_reproves(manifest, "palavras e tempos")

    def test_missing_cut_map_reproves(self):
        manifest = copy.deepcopy(self.good)
        manifest.pop("cut_map")
        self.assert_reproves(manifest, "mapa explicito")

    def test_missing_fade_reproves(self):
        manifest = copy.deepcopy(self.good)
        manifest["cut_map"][1].pop("audio_fade_out_ms")
        self.assert_reproves(manifest, "fades de audio de 30 ms")

    def test_caption_before_overlay_reproves(self):
        manifest = copy.deepcopy(self.good)
        manifest["render_order"] = ["base", "captions", "animations_overlays"]
        self.assert_reproves(manifest, "depois das animacoes")

    def test_missing_inspection_reproves(self):
        manifest = copy.deepcopy(self.good)
        manifest.pop("cut_inspections")
        self.assert_reproves(manifest, "inspecao visual")

    def test_missing_inspection_proof_reproves(self):
        manifest = copy.deepcopy(self.good)
        manifest["cut_inspections"][0]["proof"] = os.path.join(self.temp.name, "ausente.jpg")
        self.assert_reproves(manifest, "prova visual inexistente")

    def test_cut_builder_has_exact_fades_and_map(self):
        keep = [(0.0, 1.0), (2.0, 3.0)]
        filter_graph = silence.build_filter(keep)
        self.assertEqual(4, filter_graph.count("afade="))
        self.assertEqual(4, filter_graph.count("d=0.030"))
        mapped = silence.cut_map(keep)
        self.assertEqual(30, mapped[0]["audio_fade_in_ms"])
        self.assertEqual(30, mapped[1]["audio_fade_out_ms"])
        self.assertEqual(1.0, mapped[1]["timeline_start"])

    def test_legacy_negative_noise_argument_is_preserved(self):
        args = silence.parse_args(["in.mp4", "out.mp4", "-35dB", "0.40"])
        self.assertEqual("-35dB", args.noise)
        self.assertEqual("0.40", args.dur_min)

    def test_each_join_becomes_visual_target(self):
        targets = inspection.inspection_targets(self.good["cut_map"])
        self.assertEqual([("cut-002", 1.0)], targets)


if __name__ == "__main__":
    unittest.main()
