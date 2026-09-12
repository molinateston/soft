#!/usr/bin/env python3
import copy
import importlib.util
import os
import unittest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = importlib.util.spec_from_file_location(
    "visual_plan_gate", os.path.join(ROOT, "scripts", "08_gate_visual_plan.py"))
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)


class VisualPlanGateTest(unittest.TestCase):
    def setUp(self):
        self.good = gate.sample_plan()

    def assert_reproves(self, plan, fragment):
        errors = gate.validate(plan)
        self.assertTrue(any(fragment in error for error in errors), errors)

    def test_good_plan_passes(self):
        self.assertEqual([], gate.validate(self.good))

    def test_missing_phrase_decision_reproves(self):
        plan = copy.deepcopy(self.good)
        plan["decisions"][0].pop("support_phrase")
        self.assert_reproves(plan, "decisao de frase")

    def test_missing_frame_reproves(self):
        plan = copy.deepcopy(self.good)
        plan["decisions"][0].pop("first_frame")
        self.assert_reproves(plan, "first_frame")

    def test_missing_transition_reproves(self):
        plan = copy.deepcopy(self.good)
        plan["decisions"][0].pop("transition_out")
        self.assert_reproves(plan, "transition_out")

    def test_missing_time_reproves(self):
        plan = copy.deepcopy(self.good)
        plan["decisions"][0].pop("start")
        self.assert_reproves(plan, "tempos validos")

    def test_missing_speech_reproves(self):
        plan = copy.deepcopy(self.good)
        plan["decisions"][0].pop("literal_speech")
        self.assert_reproves(plan, "literal_speech")

    def test_out_of_order_time_reproves(self):
        plan = copy.deepcopy(self.good)
        plan["decisions"][1]["start"] = 5
        self.assert_reproves(plan, "ordem temporal")

    def test_missing_central_review_reproves(self):
        plan = copy.deepcopy(self.good)
        plan.pop("central_review")
        self.assert_reproves(plan, "revisao central")


if __name__ == "__main__":
    unittest.main()
