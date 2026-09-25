"""Missing/corrupt samples must not become sanitizer findings or clean runs."""
import math
import csv
from pathlib import Path
import tempfile
import unittest

from modelsan.backends.rumoca import RumocaBackend, classify
from modelsan.runtime.failures import FailureKind
from modelsan.runtime.observations import VariableObservation

HEADER = "time,trace_id,connection,variable,quantity,unit,value\n"


class TraceTransport(unittest.TestCase):
    def read(self, data):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "trace.csv"
            path.write_text(data)
            return RumocaBackend._read_trace(path)

    def test_bad_rows_and_missing_samples_are_not_invented_nans(self):
        for data in ["time,value\n0,2\n", HEADER + "0,0,,x,,\n",
                     HEADER + "nan,0,,x,,,2\n",
                     HEADER + "0,0,,x,,,2\n0,1,,y,,,3\n1,0,,x,,,4\n",
                     HEADER + "0,0,,x,,,2\n0,1,,x,,,3\n",
                     HEADER + "1,0,,x,,,2\n0,0,,x,,,3\n"]:
            with self.subTest(data=data), self.assertRaises(ValueError):
                self.read(data)

    def test_real_nonfinite_values_are_preserved(self):
        times, columns = self.read(HEADER + "0,0,,x,,,nan\n1,0,,x,,,inf\n")
        self.assertEqual(times, [0, 1])
        self.assertTrue(math.isnan(columns["x"][0]))
        self.assertEqual(columns["x"][1], math.inf)

    def test_truncated_quoted_value_is_rejected(self):
        with self.assertRaises(csv.Error):
            self.read(HEADER + '0,0,,x,,,"2\n')

    def test_duplicate_declarations_can_report_the_same_value(self):
        self.assertEqual(self.read(HEADER + "0,0,,x,,,2\n0,1,,x,,,2\n"), ([0], {"x": [2]}))

    def test_event_rows_at_one_time_are_preserved_in_publication_order(self):
        data = HEADER + "0,0,,x,,,2\n0,1,,y,,,4\n0,0,,x,,,3\n0,1,,y,,,5\n"
        self.assertEqual(self.read(data), ([0,0], {'x':[2,3], 'y':[4,5]}))

    def test_observation_order_is_time_major(self):
        backend = RumocaBackend()
        backend._ids = {"x": 0, "y": 1}
        stream = backend._stream([0, 1], {"x": [2, 3], "y": [4, 5]})
        observations = list(stream.of(VariableObservation))
        self.assertEqual([(o.time, o.canonical.name) for o in observations],
                         [(0, "x"), (0, "y"), (1, "x"), (1, "y")])

    def test_failure_words_do_not_match_substrings(self):
        self.assertEqual(classify("information unavailable"), FailureKind.UNKNOWN)
        self.assertEqual(classify("division by zero produced inf"), FailureKind.DIVISION_BY_ZERO)
        self.assertEqual(classify("value is NaN"), FailureKind.NON_FINITE_VALUE)
