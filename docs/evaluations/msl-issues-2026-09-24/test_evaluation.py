"""Evaluation integrity regressions; no compiler or production-code mutation.

Run: python3 -m unittest discover -s docs/evaluations/msl-issues-2026-09-24
     -p test_evaluation.py -v

Matching/classification tests use synthetic evidence. The catalog census is
deliberately pinned to the archived 2026-09-24 ledger, not a fabricated corpus.
"""
from copy import deepcopy
import json
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import evaluate
import matching
import runtime


def divisor_fixture():
    row = {"id": "TEST-001", "verdict": "confirmed", "model": "Modelica.Test.Driver",
           "target": "dut.p", "sanitizer_kind": "divisor-reachable-zero",
           "declaration": "Modelica/Blocks/Test.mo:42", "original": "synthetic.md"}
    evidence = {"denominator": "dut.p - dut.q", "witness": "dut.p = 2, dut.q = 2",
                "path_condition": "dut.enabled > 0"}
    finding = {"sanitizer": "divisor", "kind": "divisor-reachable-zero", "severity": "high",
               "evidence": deepcopy(evidence), "canonical_anchors": [],
               "source_locations": [{"file": "target/msl/Modelica 4.1.0/Blocks/Test.mo", "line": 42}]}
    return row, evidence, finding


def static_score(row, old, findings, status="analyzed"):
    result = {"status": status, "findings": findings, "hints": [],
              "analyses": {"divisor.analyze": {"status": "ok"}}}
    with patch.object(matching, "_original", return_value={"evidence": old, "sha256": "synthetic"}):
        return matching.score(row, result)


def runtime_result(status="failed", operation="division"):
    return {"status": status, "trace_samples": 0,
            "backend_metadata": {"domain_diagnostics": {"faults": [
                {"program_sha1": "0" * 40, "instruction_index": 3}]}},
            "findings": [{"sanitizer": "domain", "kind": f"{operation}-out-of-domain",
                          "severity": "high", "evidence": {"operation": operation},
                          "canonical_anchors": [], "backend_anchors": ["synthetic-native-site"]}]}


class MatcherIntegrity(unittest.TestCase):
    def test_exact_source_denominator_full_witness_and_path(self):
        row, old, finding = divisor_fixture()
        finding["evidence"]["denominator"] = "(dut.p - dut.q)"
        finding["evidence"]["witness"] = "dut.q = 2.0, dut.p = 2e0"
        actual = static_score(row, old, [finding])
        self.assertEqual(actual["strict_detection"], "static-defect-candidate")
        self.assertTrue(actual["exact_candidate"])
        self.assertEqual(len(actual["matched_findings"]), 1)

    def test_same_target_different_source_is_not_exact(self):
        for replacement in ({"file": "Modelica/Other/Test.mo", "line": 42},
                            {"file": "Modelica/Blocks/Test.mo", "line": 43}):
            with self.subTest(replacement=replacement):
                row, old, finding = divisor_fixture()
                finding["source_locations"] = [replacement]
                self.assert_ambiguous(row, old, finding)

    def test_same_target_different_denominator_is_not_exact(self):
        row, old, finding = divisor_fixture()
        finding["evidence"]["denominator"] = "dut.p + dut.q"
        self.assert_ambiguous(row, old, finding)

    def test_same_target_different_or_incomplete_witness_is_not_exact(self):
        for replacement in ("dut.p = 0, dut.q = 0", "dut.p = 2"):
            with self.subTest(witness=replacement):
                row, old, finding = divisor_fixture()
                finding["evidence"]["witness"] = replacement
                self.assert_ambiguous(row, old, finding)

    def test_same_target_different_branch_is_not_exact(self):
        row, old, finding = divisor_fixture()
        finding["evidence"]["path_condition"] = "dut.enabled <= 0"
        self.assert_ambiguous(row, old, finding)

    def assert_ambiguous(self, row, old, finding):
        actual = static_score(row, old, [finding])
        self.assertEqual(actual["strict_detection"], "ambiguous-site-match")
        self.assertFalse(actual["exact_candidate"])
        self.assertEqual(actual["matched_findings"], [])
        # Weaker target overlap remains visible, but cannot manufacture credit.
        self.assertEqual(len(actual["ambiguous_findings"]), 1)

    def test_metadata_and_unknown_kinds_never_default_to_defects(self):
        for kind in ("semantic-binding-conflict", "semantic-binding-ambiguous",
                     "semantic-mapping-unmatched", "future-unknown-kind"):
            with self.subTest(kind=kind):
                self.assertEqual(matching._decision([{"kind": kind}]), "unresolved-analysis")
        self.assertEqual(matching._decision([{"kind": "divisor-reachable-zero"}]),
                         "static-defect-candidate")

    def test_compiler_failure_retains_report_without_credit(self):
        row, old, finding = divisor_fixture()
        actual = static_score(row, old, [finding], status="compile-blocked")
        self.assertEqual(actual["id"], row["id"])
        self.assertEqual(actual["strict_detection"], "blocked-before-analysis")
        self.assertFalse(actual["exact_candidate"])


class SeededRuntimeIntegrity(unittest.TestCase):
    def test_every_archived_confirmed_id_is_preserved_exactly_once(self):
        cases = runtime.catalog()
        ledger = {row["id"]: row for row in json.loads(runtime.LEDGER.read_text())
                  if row["verdict"] == "confirmed"
                  and row["model"].startswith(("Modelica.", "ModelicaTest."))}
        identifiers = [identifier for case in cases for identifier in case["report_ids"]]
        self.assertEqual(len(cases), 315)
        self.assertEqual(len({case["model"] for case in cases}), 124)
        self.assertEqual(len(identifiers), 819)
        self.assertEqual(len(set(identifiers)), 819)
        self.assertEqual(set(identifiers), set(ledger))
        for case in cases:
            for identifier in case["report_ids"]:
                self.assertEqual(case["model"], ledger[identifier]["model"])

    def test_backend_error_cannot_become_a_domain_hit(self):
        actual = runtime.classify({"expected_operations": ["division"]},
                                  runtime_result(status="backend-error"))
        self.assertEqual(actual, "blocked-backend-or-configuration")

    def test_matching_operation_is_only_a_seeded_signal_not_source_identity(self):
        actual = runtime.classify({"expected_operations": ["division"]}, runtime_result())
        self.assertEqual(actual, "seeded-operation-signal")
        self.assertNotIn("exact", actual)
        self.assertNotIn("confirmed", actual)

    def test_other_operation_cannot_satisfy_expected_operation(self):
        actual = runtime.classify({"expected_operations": ["log"]}, runtime_result())
        self.assertEqual(actual, "symptom-only")

    def test_runtime_configuration_eligibility_does_not_claim_source_equivalence(self):
        contract = SimpleNamespace(is_final=False, is_protected=False, structural=False,
                                   binding_depends_on=())
        variable = SimpleNamespace(name="p", id=0, role="parameter", is_parameter=True,
                                   tunable=True, scalar_count=1, contract=contract)
        model = SimpleNamespace(variables=[variable], has_execution=False)
        actual = runtime.configuration(model, {"parameters": {"p": 0.0}})
        self.assertTrue(actual["eligible"])
        self.assertIn("does not prove source-recompile equivalence", actual["scope"])


class CollectionFreshness(unittest.TestCase):
    def collected_status(self, *, checkpoint_id="current", checkpoint_time=200,
                         requested=True, worker=True, validation="run-id", log_time=200):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            out, docs = root / "corpus", root / "docs"
            docs.mkdir()
            model = "Modelica.Test.Driver"
            ledger = root / "ledger.json"
            ledger.write_text(json.dumps([{"id": "TEST-001", "model": model,
                                           "verdict": "confirmed", "target": "p"}]))
            directory = out / evaluate.key(model)
            directory.mkdir(parents=True)
            checkpoint = {"model": model, "status": "analyzed", "campaign_id": checkpoint_id}
            if worker:
                checkpoint["worker"] = {"exit": 0}
            path = directory / "static.json"
            path.write_text(json.dumps(checkpoint))
            os.utime(path, (checkpoint_time, checkpoint_time))
            if log_time is not None:
                log = directory / "worker.log"
                log.write_text("synthetic completed worker\n")
                os.utime(log, (log_time, log_time))
            campaign = {"id": "current", "started_epoch": 100, "validation": validation,
                        "models": [model] if requested else []}
            def fake_score(row, result):
                return {**row, "detection": "blocked-before-analysis",
                        "strict_detection": "blocked-before-analysis", "analysis_status": result["status"]}
            with patch.object(evaluate, "OUT", out), patch.object(evaluate, "LEDGER", ledger), \
                 patch.object(evaluate, "__file__", str(docs / "evaluate.py")), \
                 patch.object(evaluate, "score", side_effect=fake_score), \
                 patch.object(evaluate.subprocess, "check_output", return_value="synthetic-head\n"):
                evaluate.collect(campaign)
            results = json.loads((docs / "model-results.json").read_text())
            reports = json.loads((docs / "corpus-results.json").read_text())["reports"]
            self.assertEqual([r["id"] for r in reports], ["TEST-001"])
            return results[0]["status"]

    def test_matching_current_campaign_is_eligible(self):
        self.assertEqual(self.collected_status(), "analyzed")

    def test_wrong_campaign_old_timestamp_and_unrequested_model_are_blocked(self):
        for changes in ({"checkpoint_id": "old"}, {"checkpoint_time": 50}, {"requested": False}):
            with self.subTest(changes=changes):
                self.assertEqual(self.collected_status(**changes), "outside-requested-run-or-stale-checkpoint")

    def test_incomplete_worker_is_not_collected_as_analyzed(self):
        self.assertEqual(self.collected_status(worker=False), "incomplete-worker")

    def test_timestamp_adoption_requires_fresh_worker_log_too(self):
        for log_time in (None, 50):
            with self.subTest(log_time=log_time):
                self.assertEqual(self.collected_status(validation="timestamp", log_time=log_time),
                                 "outside-requested-run-or-stale-checkpoint")
        self.assertEqual(self.collected_status(validation="timestamp"), "analyzed")


if __name__ == "__main__":
    unittest.main()
