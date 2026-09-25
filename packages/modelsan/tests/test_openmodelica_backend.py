"""Execution and trace failures must not masquerade as successful evidence."""

import math
import hashlib
import os
from pathlib import Path
import signal
import subprocess
import tempfile
import unittest
from unittest.mock import Mock, patch

from modelsan.backends.base import ExecutionStatus
from modelsan.backends.csv_trace import UnorderedTraceError, read_csv_trace
from modelsan.backends.openmodelica import OpenModelicaBackend, _modelica_string
from modelsan.backends.process import execute
from modelsan.fuzz.testcase import TestCase
from modelsan.runtime.failures import ExecutionPhase, FailureKind
from modelsan.runtime.observations import SimulationAbort, UnorderedVariableObservation, VariableObservation


class OpenModelicaExecution(unittest.TestCase):
    def setUp(self):
        self.backend = OpenModelicaBackend([], timeout=0.25, number_of_intervals=400)
        self.addCleanup(self.backend.close)

    def prepared(self):
        self.backend._work = tempfile.TemporaryDirectory()
        work = Path(self.backend._work.name)
        self.backend._executable = work / "modelsan_model"
        self.backend._executable.write_text("fake model")
        self.backend._executable.chmod(0o755)
        return work

    def completed(self, returncode=0, stdout="", stderr=""):
        return subprocess.CompletedProcess(["fake"], returncode, stdout, stderr)

    def test_reprepare_failure_cannot_run_previous_model(self):
        previous = self.prepared()
        with patch("modelsan.backends.openmodelica.execute", return_value=self.completed()):
            result = self.backend.prepare("source.mo", "Broken")
        self.assertEqual(result.status, ExecutionStatus.BACKEND_ERROR)
        self.assertFalse(previous.exists())
        self.assertIsNone(self.backend._executable)
        self.assertEqual(self.backend.run(TestCase()).status, ExecutionStatus.BACKEND_ERROR)

    def test_prepare_respects_timeout_intervals_and_quoted_paths(self):
        def build(command, work, timeout, **kwargs):
            script = (work / "build.mos").read_text()
            self.assertEqual(timeout, 0.25)
            self.assertIn("numberOfIntervals=400", script)
            self.assertIn(r'quoted\"path.mo', script)
            model = work / "modelsan_model"
            model.write_text("fake model")
            model.chmod(0o755)
            return self.completed()

        with patch("modelsan.backends.openmodelica.execute", side_effect=build):
            self.assertIsNone(self.backend.prepare('quoted"path.mo', "Package.Model"))

    def test_build_failure_retains_full_diagnostics_even_if_executable_exists(self):
        def failed_build(command, work, timeout, **kwargs):
            model = work / "modelsan_model"
            model.write_text("incomplete executable")
            model.chmod(0o755)
            return self.completed(1, "diagnostic\n" * 100, "link failed\n")

        with patch("modelsan.backends.openmodelica.execute", side_effect=failed_build):
            result = self.backend.prepare("source.mo", "Model")
        self.assertEqual(result.status, ExecutionStatus.BACKEND_ERROR)
        self.assertEqual(result.backend_metadata["stdout"], "diagnostic\n" * 100)
        self.assertIn("link failed\n", result.failure.raw)
        self.assertIsNone(self.backend._executable)

    def test_build_timeout_is_backend_error_with_output(self):
        timeout = subprocess.TimeoutExpired(["omc"], 0.25, output="build stage\n", stderr="unfinished\n")
        with patch("modelsan.backends.openmodelica.execute", side_effect=timeout):
            result = self.backend.prepare("source.mo", "Model")
        self.assertEqual(result.status, ExecutionStatus.BACKEND_ERROR)
        self.assertEqual(result.phase, ExecutionPhase.COMPILATION)
        self.assertIn("build stage\nunfinished\n", result.failure.raw)

    def test_missing_omc_or_simulator_is_backend_error(self):
        with patch("modelsan.backends.openmodelica.execute", side_effect=FileNotFoundError("omc")):
            result = self.backend.prepare("source.mo", "Model")
        self.assertEqual(result.status, ExecutionStatus.BACKEND_ERROR)
        self.backend.close()
        self.prepared()
        self.backend._executable.unlink()
        self.assertEqual(self.backend.run(TestCase()).status, ExecutionStatus.BACKEND_ERROR)

    def test_stale_csv_is_removed_before_each_execution(self):
        work = self.prepared()
        (work / "modelsan_model_res.csv").write_text("time,x\n0,2\n")
        with patch("modelsan.backends.openmodelica.execute", return_value=self.completed(1, "no convergence\n")):
            result = self.backend.run(TestCase())
        self.assertEqual(result.status, ExecutionStatus.FAILED)
        self.assertEqual(result.failure.kind, FailureKind.NONLINEAR_SOLVER_FAILURE)
        self.assertIsNone(result.trace)
        self.assertEqual(result.failure.raw, "no convergence\n")

    def test_exit_zero_without_trace_is_backend_error(self):
        self.prepared()
        with patch("modelsan.backends.openmodelica.execute", return_value=self.completed()):
            result = self.backend.run(TestCase())
        self.assertEqual(result.status, ExecutionStatus.BACKEND_ERROR)
        self.assertIn("no trace", result.failure.raw)

    def test_corrupt_trace_does_not_invent_nan_findings(self):
        work = self.prepared()

        def simulate(*args, **kwargs):
            (work / "modelsan_model_res.csv").write_text("time,x\n0,bad\n")
            return self.completed(stdout="completed\n")

        with patch("modelsan.backends.openmodelica.execute", side_effect=simulate):
            result = self.backend.run(TestCase())
        self.assertEqual(result.status, ExecutionStatus.BACKEND_ERROR)
        self.assertIsNone(result.trace)
        self.assertEqual(list(result.observations.of(VariableObservation)), [])
        self.assertEqual(result.backend_metadata["stdout"], "completed\n")

    def test_unordered_times_preserve_values_and_exact_csv_without_a_trajectory(self):
        work = self.prepared()
        csv_text = '"time","x"\n0,0\n0.1,0\n0.1,1\n0.09999999999999999,1\n0.2,2\n'

        def simulate(*args, **kwargs):
            (work / "modelsan_model_res.csv").write_text(csv_text)
            return self.completed(stdout="completed\n")

        with patch("modelsan.backends.openmodelica.execute", side_effect=simulate):
            result = self.backend.run(TestCase())
        self.assertTrue(result.ok)
        self.assertIsNone(result.trace)
        self.assertEqual(list(result.observations.of(VariableObservation)), [])
        samples = list(result.observations.of(UnorderedVariableObservation))
        self.assertEqual([s.value for s in samples], [0, 0, 1, 1, 2])
        self.assertEqual([s.reported_time for s in samples], [0, 0.1, 0.1, 0.09999999999999999, 0.2])
        self.assertEqual([s.row_index for s in samples], [0, 1, 2, 3, 4])
        self.assertTrue(all(s.time is None for s in samples))
        evidence = result.backend_metadata["temporal_trace"]
        self.assertFalse(evidence["available"])
        self.assertEqual(evidence["raw_csv"], csv_text)
        self.assertEqual(evidence["raw_csv_sha256"], hashlib.sha256(csv_text.encode()).hexdigest())

    def test_time_reversal_does_not_hide_later_malformed_data(self):
        work = self.prepared()

        def simulate(*args, **kwargs):
            (work / "modelsan_model_res.csv").write_text("time,x\n1,2\n0,3\n0.1,bad\n")
            return self.completed()

        with patch("modelsan.backends.openmodelica.execute", side_effect=simulate):
            result = self.backend.run(TestCase())
        self.assertEqual(result.status, ExecutionStatus.BACKEND_ERROR)
        self.assertEqual(list(result.observations.of(UnorderedVariableObservation)), [])

    def test_success_retains_override_semantics_events_and_nonfinite_samples(self):
        work = self.prepared()

        def simulate(command, *args, **kwargs):
            self.assertEqual(command[-2:], ["-override", "p=3,x=4"])
            (work / "modelsan_model_res.csv").write_text("time,x,y\n0,1,2\n0.5,nan,3\n")
            return self.completed(stdout="time event at time=0.5\n")

        case = TestCase(parameters={"p": 2}, initial_values={"p": 3, "x": 4})
        with patch("modelsan.backends.openmodelica.execute", side_effect=simulate):
            result = self.backend.run(case)
        self.assertTrue(result.ok)
        self.assertTrue(math.isnan(result.trace.columns["x"][-1]))
        self.assertEqual([event.time for event in result.events], [0.5])
        observations = list(result.observations.of(VariableObservation))
        self.assertEqual([(item.time, item.backend.name) for item in observations],
                         [(0, "x"), (0, "y"), (0.5, "x"), (0.5, "y")])

    def test_runtime_timeout_keeps_partial_output(self):
        self.prepared()
        timeout = subprocess.TimeoutExpired(["model"], 0.25, output="sample\n", stderr="solver\n")
        with patch("modelsan.backends.openmodelica.execute", side_effect=timeout):
            result = self.backend.run(TestCase())
        self.assertEqual(result.status, ExecutionStatus.TIMEOUT)
        self.assertEqual(result.failure.raw, "sample\nsolver\n")

    def test_signal_termination_is_aborted_even_with_truncated_trace(self):
        work = self.prepared()

        def interrupted(*args, **kwargs):
            (work / "modelsan_model_res.csv").write_text("time,x\n0,1\n0.1,")
            return self.completed(-9, "last runtime message\n", "interrupted\n")

        with patch("modelsan.backends.openmodelica.execute", side_effect=interrupted):
            result = self.backend.run(TestCase())
        self.assertEqual(result.status, ExecutionStatus.ABORTED)
        self.assertEqual(result.failure.kind, FailureKind.ABORTED)
        self.assertEqual(result.failure.raw, "last runtime message\ninterrupted\n")
        self.assertEqual(result.backend_metadata["signal"], 9)
        self.assertIsNone(result.trace)
        observations = list(result.observations.of(SimulationAbort))
        self.assertEqual(len(observations), 1)
        self.assertEqual(observations[0].kind, FailureKind.ABORTED)
        self.assertEqual(observations[0].raw, result.failure.raw)

    def test_model_name_cannot_inject_mos_statements(self):
        with patch("modelsan.backends.openmodelica.execute") as launch:
            result = self.backend.prepare("source.mo", "M); system(\"unexpected\"); buildModel(M")
        self.assertEqual(result.status, ExecutionStatus.BACKEND_ERROR)
        launch.assert_not_called()

    def test_string_literal_escapes_paths_deterministically(self):
        self.assertEqual(_modelica_string('a\\b"c\n'), '"a\\\\b\\"c\\n"')
        with self.assertRaises(ValueError):
            _modelica_string("bad\x00path")


class DenseCsvTrace(unittest.TestCase):
    def read(self, data):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "trace.csv"
            path.write_text(data)
            return read_csv_trace(path)

    def test_invalid_shapes_names_and_time_are_rejected(self):
        bad = ["", "x\n1\n", "time,x,x\n0,1,2\n", "time,\n0,1\n",
               "time,x\n0\n", "time,x\n0,1,2\n", "time,x\n0,abc\n",
               "time,x\nnan,1\n", "time,x\ninf,1\n", "time,x\n1,2\n0,3\n"]
        for data in bad:
            with self.subTest(data=data), self.assertRaises(ValueError):
                self.read(data)

    def test_event_sides_are_preserved_and_nonnumeric_cells_are_not_repaired(self):
        times, columns = self.read('"time","x","a[1,2]"\n0,1,3\n0,2,4\n1,inf,nan\n')
        self.assertEqual(times, [0, 0, 1])
        self.assertEqual(columns["x"], [1, 2, math.inf])
        self.assertTrue(math.isnan(columns["a[1,2]"][-1]))

    def test_even_one_ulp_reversal_is_not_a_trajectory(self):
        for second in (0.09999999999999999, 0.05):
            with self.subTest(second=second), self.assertRaises(UnorderedTraceError) as caught:
                self.read(f"time,x\n0.1,1\n0.1,2\n{second},3\n")
            self.assertEqual(caught.exception.samples.times, [0.1, 0.1, second])
            self.assertEqual(caught.exception.samples.columns["x"], [1, 2, 3])

    def test_bad_time_or_shape_cannot_become_unordered_value_evidence(self):
        for ending in ("nan,4\n", "inf,4\n", "0.2,\n", "0.2,4,5\n"):
            with self.subTest(ending=ending), self.assertRaises(ValueError) as caught:
                self.read("time,x\n1,2\n0,3\n" + ending)
            self.assertNotIsInstance(caught.exception, UnorderedTraceError)


class BoundedProcesses(unittest.TestCase):
    @unittest.skipUnless(os.name == "posix", "process groups are a POSIX facility")
    def test_timeout_kills_entire_process_group_and_drains_output(self):
        process = Mock(pid=321, returncode=-9)
        process.communicate.side_effect = [subprocess.TimeoutExpired(["tool"], 0.25),
                                           ("partial stdout\n", "partial stderr\n")]
        with patch("modelsan.backends.process.subprocess.Popen", return_value=process) as launch:
            with patch("modelsan.backends.process.os.killpg") as kill:
                with self.assertRaises(subprocess.TimeoutExpired) as caught:
                    execute(["tool"], Path("."), 0.25)
        kill.assert_called_once_with(321, signal.SIGKILL)
        self.assertTrue(launch.call_args.kwargs["start_new_session"])
        self.assertEqual(caught.exception.stdout, "partial stdout\n")
        self.assertEqual(caught.exception.stderr, "partial stderr\n")
        self.assertEqual(process.communicate.call_count, 2)


if __name__ == "__main__":
    unittest.main()
