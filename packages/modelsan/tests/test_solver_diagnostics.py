"""Native owner evidence is not inferred from the publication grid."""
from pathlib import Path
import tempfile
import unittest

from modelsan.backends.rumoca import RumocaBackend
from modelsan.backends.rumoca_diagnostics import read_solver
from modelsan.fuzz.testcase import NOMINAL
from modelsan.runtime.observations import (
    EquationResidual, EventTriggered, JacobianObservation, ObservationStream, SolverStep,
)
from rumoca_bitcode.execution import lower
from test_current_bitcode import decay, RUMOCA


class SolverDiagnostics(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.backend = RumocaBackend(RUMOCA, t_end=.2)
        self.addCleanup(self.backend.close)

    def test_native_steps_are_not_output_samples(self):
        path = self.root / "decay.rbc"
        lower(decay()).save(path)
        self.assertIsNone(self.backend.prepare_from_artifact(path))
        result = self.backend.run(NOMINAL)
        self.assertTrue(result.ok, result.failure)
        steps = list(result.observations.of(SolverStep))
        self.assertTrue(steps)
        self.assertTrue(all(s.coordinates == "accepted-proposal" for s in steps))
        self.assertNotEqual(len(steps), len(result.trace.times))
        self.assertEqual(list(result.observations.of(EventTriggered)), [])

    def test_actual_time_event_is_observed(self):
        path = self.root / "Pulse.mo"
        path.write_text('''model Pulse
  Real x(start=0, fixed=true);
  discrete Real d(start=0, fixed=true);
equation
  der(x) = d;
  when time >= 0.1 then
    d = 1;
  end when;
end Pulse;
''')
        failure = self.backend.prepare(str(path), "Pulse")
        self.assertIsNone(failure, str(failure))
        result = self.backend.run(NOMINAL)
        self.assertTrue(result.ok, result.failure)
        events = list(result.observations.of(EventTriggered))
        self.assertTrue(events)
        self.assertAlmostEqual(events[0].time, .1, places=7)
        self.assertAlmostEqual(result.trace.final_state["x"], .1, places=6)

    def test_projection_transport_keeps_trial_coordinates_and_no_fake_rank(self):
        stream = ObservationStream()
        evidence = {"schema_version": 1, "coordinates": "native-internal", "omitted": 0,
            "coverage": "me-accepted-proposals-events-projection-blocks", "records": [
            {"kind": "projection", "phase": "initialization", "time": 0.,
             "row_count": 1, "column_count": 1, "values_omitted": False,
             "rows": [2], "columns": [3], "residual": [4.], "jacobian_column_major": [5.]}]}
        read_solver(evidence, stream)
        residual = list(stream.of(EquationResidual))[0]
        self.assertIsNone(residual.canonical)
        self.assertEqual(residual.coordinates, "internal-initialization")
        matrix = list(stream.of(JacobianObservation))[0]
        self.assertEqual(matrix.values_column_major, [5.])
        self.assertIsNone(matrix.rank)
        self.assertIsNone(matrix.condition_estimate)
        evidence["records"][0]["jacobian_column_major"] = []
        with self.assertRaises(ValueError):
            read_solver(evidence, ObservationStream())

    def test_projection_values_come_from_a_native_coupled_solve(self):
        path = self.root / "Coupled.mo"
        path.write_text('''model Coupled
  Real x(start=2, fixed=true);
  Real z(start=1);
  Real w(start=0);
equation
  der(x) = -x;
  z*z + w = x;
  z + w = 1;
end Coupled;
''')
        self.assertIsNone(self.backend.prepare(str(path), "Coupled"))
        result = self.backend.run(NOMINAL)
        self.assertTrue(result.ok, result.failure)
        matrices = list(result.observations.of(JacobianObservation))
        self.assertTrue(matrices)
        self.assertTrue(list(result.observations.of(EquationResidual)))
        self.assertTrue(all(m.coordinates.startswith("internal-") for m in matrices))

    def test_unsupported_clocked_import_is_not_a_model_bug(self):
        from modelsan.backends.base import ExecutionStatus
        path = self.root / "Clocked.mo"
        path.write_text('''model Clocked
  Real x(start=0, fixed=true);
  discrete Real d(start=0, fixed=true);
equation
  der(x) = d;
  when sample(0.1, 0.1) then
    d = pre(d) + 1;
  end when;
end Clocked;
''')
        failure = self.backend.prepare(str(path), "Clocked")
        result = failure if failure is not None else self.backend.run(NOMINAL)
        self.assertEqual(result.status, ExecutionStatus.BACKEND_ERROR)
