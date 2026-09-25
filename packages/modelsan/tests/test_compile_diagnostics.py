"""Model findings need typed compiler proof; compilation failure alone is not one."""
import json
from pathlib import Path
import tempfile
import unittest

from modelsan.backends.compile_diagnostics import proven_model_failure
from modelsan.campaign import run_case
from modelsan.runtime.failures import FailureKind
from test_campaign import Backend


class CompilerEvidence(unittest.TestCase):
    def read(self, report):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'diagnostics.json'
            path.write_text(json.dumps(report))
            return proven_model_failure(path, 'native')

    def report(self, code='EF032'):
        return dict(schema=1, status='failed', diagnostics=[dict(code=code,
            message='array index out of bounds: index 2, size 1',
            labels=[dict(file='library.mo', line=12, column=3)], notes=[])])

    def test_exact_proof_is_a_compilation_finding_without_execution(self):
        result = self.read(self.report())
        self.assertEqual(result.failure.kind, FailureKind.ARRAY_BOUNDS)
        report = run_case(Backend(None, preparation=result), '', 'M', [])
        self.assertEqual(report['status'], 'model-rejected')
        self.assertEqual(report['executions'][0]['phase'], 'compilation')
        finding = report['findings'][0]
        self.assertEqual(finding['kind'], 'compile-time-array-bounds')
        self.assertEqual(finding['evidence']['compiler_diagnostic']['code'], 'EF032')
        self.assertFalse(finding['evidence']['tool_side'])
        self.assertEqual(finding['source_locations'],
                         [dict(file='library.mo', line=12, column=3)])

    def test_identical_prose_with_unknown_or_tool_code_is_not_a_model_proof(self):
        for code in ['ED008','EF005','EF015',None,'EF032_extra']:
            self.assertIsNone(self.read(self.report(code)))
        report = self.report()
        report['status'] = 'success'
        self.assertIsNone(self.read(report))

    def test_incomplete_proof_and_unknown_schema_are_rejected(self):
        for field, value in [('labels',[]), ('labels',[{}]),
                             ('labels',[dict(file=None,line=1,column=1)]),
                             ('labels',[dict(file='x.mo',line=0,column=1)]),
                             ('labels',[dict(file='x.mo',line=True,column=1)]),
                             ('message','')]:
            report = self.report()
            report['diagnostics'][0][field] = value
            with self.assertRaises(ValueError):
                self.read(report)
        report = self.report()
        report['schema'] = 99
        with self.assertRaises(ValueError):
            self.read(report)


if __name__ == '__main__':
    unittest.main()
