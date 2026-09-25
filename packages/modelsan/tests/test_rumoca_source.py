"""Native source observations must be genuine and explicitly scoped."""
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from modelsan.backends.base import ExecutionStatus
from modelsan.backends.rumoca_source import RumocaSourceBackend
from modelsan.fuzz.testcase import NOMINAL, TestCase as Case
from modelsan.instrumentation.capability import Capability
from modelsan.instrumentation.request import InstrumentationRequest
from modelsan.runtime.anchors import CanonicalAnchor, EntityKind
from modelsan.runtime.failures import FailureKind
from modelsan.runtime.observations import VariableObservation

ROOT = Path(__file__).resolve().parents[3]
RUMOCA = Path(os.environ.get("RUMOCA", ROOT / "target/debug/rumoca")).resolve()
MSL = ROOT / "target/msl/ModelicaStandardLibrary-4.1.0"
PROBES = ROOT / "docs/evaluations/msl-upstream-open-issues-2026-09-24/SemanticProbes.mo"


class RumocaSourceContract(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.source = Path(self.tmp.name) / "Test.mo"
        self.source.write_text("model Test Real x; equation x = time; end Test;")
        self.backend = RumocaSourceBackend(sys.executable, t_end=1, timeout=2,
                                          source_roots=[self.tmp.name], cache_dir=self.tmp.name)
        self.addCleanup(self.backend.close)
        self.assertIsNone(self.backend.prepare(str(self.source), "Test"))

    def execute(self, payload="time,x,y\n0,1,2\n.5,3,4\n.5,5,6\n1,7,8\n",
                returncode=0, stderr=""):
        def launch(command, work, timeout, *, env=None):
            if payload is not None:
                Path(command[command.index("--output") + 1]).write_text(payload)
            return subprocess.CompletedProcess(command, returncode, "", stderr)
        return patch("modelsan.backends.rumoca_source.execute", side_effect=launch)

    def test_nominal_trace_has_backend_identity_event_sides_and_time_order(self):
        with self.execute() as invoke:
            result = self.backend.run(NOMINAL)
        self.assertTrue(result.ok, result.failure)
        self.assertEqual(result.trace.times, [0, .5, .5, 1])
        observations = list(result.observations.of(VariableObservation))
        self.assertEqual([(v.time, v.backend.name) for v in observations],
                         [(t, name) for t in [0, .5, .5, 1] for name in ["x", "y"]])
        self.assertTrue(all(v.canonical is None for v in observations))
        self.assertTrue(all(v.backend.backend == "rumoca-source" for v in observations))
        self.assertNotIn(Capability.CANONICAL_MODEL, self.backend.capabilities)
        self.assertNotIn(Capability.CANONICAL_IDENTITY, self.backend.capabilities)
        command = invoke.call_args.args[0]
        self.assertEqual(command[1:3], ["sim", str(self.source)])
        self.assertIn("--source-root", command)
        self.assertEqual(result.backend_metadata["identity"], "backend-only")
        self.assertEqual(len(result.backend_metadata["source_sha256"]), 64)

    def test_refuses_every_unsupported_override_before_launch(self):
        cases = [Case(parameters={"x": 1}), Case(initial_values={"x": 1}),
                 Case(input_trajectory=[]), Case(solver_options={"rtol": 1e-4})]
        with self.execute() as invoke:
            for case in cases:
                self.assertEqual(self.backend.run(case).status, ExecutionStatus.BACKEND_ERROR)
        invoke.assert_not_called()

    def test_fixed_parameter_profile_is_explicit_and_reported(self):
        self.backend.freeze_parameters = True
        self.assertIsNone(self.backend.prepare(str(self.source), "Test"))
        with self.execute() as invoke:
            result = self.backend.run(NOMINAL)
        self.assertIn('--freeze-parameters', invoke.call_args.args[0])
        self.assertEqual(result.backend_metadata['parameter_policy'], 'frozen')

    def test_typed_compile_proof_survives_without_a_runtime_trace(self):
        import json
        def launch(command, work, timeout, *, env=None):
            report = dict(schema=1, status='failed', diagnostics=[dict(code='EF032',
                message='array index out of bounds: index 2, size 1',
                labels=[dict(file=str(self.source), line=1, column=1)], notes=[])])
            Path(command[command.index('--diagnostics-json')+1]).write_text(json.dumps(report))
            return subprocess.CompletedProcess(command, 1, '', 'human rendering')
        with patch('modelsan.backends.rumoca_source.execute', side_effect=launch):
            result = self.backend.run(NOMINAL)
        self.assertEqual(result.status, ExecutionStatus.FAILED)
        self.assertEqual(result.failure.kind, FailureKind.ARRAY_BOUNDS)
        self.assertIsNone(result.trace)
        self.assertEqual(result.backend_metadata['proof_stage'], 'constant-evaluation')

    def test_canonical_requests_and_unavailable_capabilities_are_rejected(self):
        requests = [InstrumentationRequest(Capability.OBSERVE_VARIABLE,
                        CanonicalAnchor(EntityKind.VARIABLE, 1, "x")),
                    InstrumentationRequest(Capability.OBSERVE_EVENTS)]
        with self.execute() as invoke:
            for request in requests:
                result = self.backend.run(NOMINAL, [request])
                self.assertEqual(result.status, ExecutionStatus.BACKEND_ERROR)
        invoke.assert_not_called()

    def test_malformed_and_missing_trace_are_backend_errors_not_synthetic_nans(self):
        for payload in [None, "time,x\n", "time\n0\n", "time,x\n0\n",
                        "time,x\n0,nonsense\n", 'time,x\n0,"unterminated\n']:
            with self.subTest(payload=payload), self.execute(payload):
                result = self.backend.run(NOMINAL)
                self.assertEqual(result.status, ExecutionStatus.BACKEND_ERROR)
                self.assertFalse(result.observations.has_trace)

    def test_real_nonfinite_evidence_is_preserved(self):
        with self.execute("time,x\n0,nan\n1,inf\n"):
            result = self.backend.run(NOMINAL)
        self.assertTrue(result.ok)
        self.assertTrue(math.isnan(result.trace.columns["x"][0]))
        self.assertEqual(result.trace.columns["x"][1], math.inf)

    def test_failed_or_closed_preparation_cannot_reuse_previous_source(self):
        self.assertIsNotNone(self.backend.prepare(str(self.source.with_suffix(".rbc")), "Test"))
        self.assertEqual(self.backend.run(NOMINAL).status, ExecutionStatus.BACKEND_ERROR)
        self.assertIsNone(self.backend.prepare(str(self.source), "Test"))
        self.backend.close()
        self.assertEqual(self.backend.run(NOMINAL).status, ExecutionStatus.BACKEND_ERROR)

    def test_source_change_invalidates_provenance(self):
        self.source.write_text("model Changed end Changed;")
        with self.execute() as invoke:
            result = self.backend.run(NOMINAL)
        self.assertEqual(result.status, ExecutionStatus.BACKEND_ERROR)
        invoke.assert_not_called()

    def test_compile_and_preparation_errors_are_never_model_failures(self):
        for diagnostic in ["[ED008] unresolved reference", "[EX002] singular preparation",
                           "[EL002] unsupported clock"]:
            with self.subTest(diagnostic=diagnostic), self.execute(None, 1, diagnostic):
                result = self.backend.run(NOMINAL)
                self.assertEqual(result.status, ExecutionStatus.BACKEND_ERROR)
                self.assertFalse(result.informative)

    def test_runtime_code_preserves_assert_failure_as_an_observation(self):
        with self.execute(None, 1, "[EX001] Modelica assert failed at t=0.1: required x > 0"):
            result = self.backend.run(NOMINAL)
        self.assertEqual(result.status, ExecutionStatus.FAILED)
        self.assertEqual(result.failure.kind, FailureKind.ASSERTION_VIOLATED)
        self.assertEqual(result.observations.failures[0].kind, FailureKind.ASSERTION_VIOLATED)

    def test_watchdog_with_unknown_phase_is_coverage_error(self):
        error = subprocess.TimeoutExpired(["rumoca"], 2, output="working", stderr="still working")
        with patch("modelsan.backends.rumoca_source.execute", side_effect=error):
            result = self.backend.run(NOMINAL)
        self.assertEqual(result.status, ExecutionStatus.BACKEND_ERROR)
        self.assertEqual(result.backend_metadata["timeout_seconds"], 2)
        self.assertEqual(result.backend_metadata["raw_output"], "workingstill working")


@unittest.skipUnless(RUMOCA.is_file(), "requires local Rumoca binary")
class NativeSourceFailureEvidence(unittest.TestCase):
    def test_reached_assertion_remains_a_runtime_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "Fail.mo"
            source.write_text('model Fail Real x; equation x=time; '
                              'assert(time<0.05,"reached assertion"); end Fail;')
            backend = RumocaSourceBackend(str(RUMOCA), t_end=.1, timeout=20)
            self.addCleanup(backend.close)
            self.assertIsNone(backend.prepare(str(source), "Fail"))
            result = backend.run(NOMINAL)
            self.assertEqual(result.status, ExecutionStatus.FAILED, result.failure)
            self.assertEqual(result.failure.kind, FailureKind.ASSERTION_VIOLATED)
            self.assertIn("reached assertion", result.failure.raw)


@unittest.skipUnless(RUMOCA.is_file() and MSL.is_dir() and PROBES.is_file(),
                     "requires local Rumoca binary and MSL 4.1.0 source")
class NativeMslBehaviorEvidence(unittest.TestCase):
    def test_actual_event_and_clocked_library_traces_are_observable(self):
        with tempfile.TemporaryDirectory() as directory:
            backend = RumocaSourceBackend(str(RUMOCA), source_roots=[MSL],
                                          cache_dir=directory, timeout=40)
            self.addCleanup(backend.close)
            for case in ["PulseControl", "PulsePast", "Delay", "Quantization"]:
                with self.subTest(case=case):
                    self.assertIsNone(backend.prepare(str(PROBES), "SemanticProbes." + case))
                    result = backend.run(NOMINAL)
                    self.assertTrue(result.ok, result.failure)
                    self.assertTrue(result.observations.has_trace)
                    self.assertTrue(all(v.canonical is None for v in
                                        result.observations.of(VariableObservation)))
                    if case == "Quantization":
                        self.assertEqual(sorted(set(result.trace.columns["dut.y"])),
                                         [-1, -.5, 0, .5, 1])
                        continue
                    target = .175 if case == "Delay" else .1
                    row = min(range(len(result.trace.times)),
                              key=lambda i: abs(result.trace.times[i] - target))
                    expected = {"PulseControl": 1, "PulsePast": 0,
                                "Delay": math.sin(2 * math.pi * .15)}[case]
                    self.assertAlmostEqual(result.trace.columns["actual"][row], expected, places=9)
