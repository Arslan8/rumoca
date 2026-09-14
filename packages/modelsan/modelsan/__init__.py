"""ModelSan — a bug finder for Modelica models.

ModelSan is not a linter. It does not care whether a model is syntactically
valid; the compiler settles that. It looks for parameter values, initial states
and execution conditions under which a *valid* model behaves incorrectly.

The architecture has one semantic representation — Rumoca's canonical DAE
bitcode — and thin layers around it:

    dae/              bindings over the canonical DAE. Not a second IR.
    analysis/         shared, cached analyses. Results, not representations.
    passes/           explicit DAE transformations
    instrumentation/  what to observe, and planning it against a backend
    runtime/          the observation vocabulary
    sanitizers/       what constitutes a violation
    fuzz/             test-case generation, independent of sanitizers
    backends/         execution; all tool-specific detail stops here
    findings/         one Finding shape, signatures, deduplication
    reporting/        the only place findings become output

A sanitizer defines what a violation is. It does not know how the DAE is
serialized, how a tool is launched, how tests are generated, or how findings
are printed.
"""

from .analysis import AnalysisContext
from .findings import Bug, BugDatabase, Finding, Severity
from .fuzz import NOMINAL, FuzzHint, TestCase
from .pipeline import Pipeline, RunOutcome
from .sanitizers import DomainSan, NumericSan, RangeSan, SanitizerRegistry

__all__ = [
    "AnalysisContext", "Bug", "BugDatabase", "DomainSan", "Finding", "FuzzHint",
    "NOMINAL", "NumericSan", "Pipeline", "RangeSan", "RunOutcome",
    "SanitizerRegistry", "Severity", "TestCase",
]
