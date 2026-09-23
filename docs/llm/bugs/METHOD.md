# Method and limitations

## Scope

This was a targeted parameter-domain and source-denominator audit of the local
MSL 4.1.0 snapshot. Candidate generation used source inspection and the current
static-finding inventory, but every promoted result was re-read in MSL source
and exercised with a new minimal or example-derived probe. Existing report
labels were not accepted as proof.

The audit looked especially for public parameters that participate in array
dimensions, subscripts, periods, transfer-function denominators, or protected
parameter bindings without a matching domain contract.

## Controls against false positives

- Invalid values are set in source before translation, not injected only as
  runtime overrides.
- Every invalid probe has a near-identical nominal control.
- The exact local MSL package is put first on `MODELICAPATH`; the harness prints
  `MSL 4.1.0` before running.
- A failure is attributed only when the diagnostic names the MSL-owned
  expression or when direct inspection establishes the same expression.
- Translation-created quotients, inactive conditional branches, supported zero
  limits, inherited constraints, and documented sentinels are excluded.
- Repeated downstream instances are collapsed into one root-cause report.

One useful negative control was `Thyristor.VDRM=0`: OpenModelica successfully
simulated the grounded probe while Rumoca produced a non-finite algebraic
projection. That disagreement was **not** promoted as an MSL bug.

## Evidence strength

`LLM-BUG-001` through `003` have nominal execution and invalid-case evidence
from both tools. `LLM-BUG-004` and `005` have complete OpenModelica execution
controls; Rumoca independently accepts the nominal source but rejects the
invalid source at the same constant division. Rumoca cannot currently complete
the nominal runtime for those two probes for unrelated implementation reasons,
which is stated in their reports.

## Limitations

This is not an exhaustive proof that the rest of MSL is bug-free. It does not
promote static-only physical-domain opinions, and it does not claim upstream
maintainers intended one particular repair. For each issue, the library may
either reject the invalid value or explicitly implement and document a limit;
the defect is that the current public contract admits a value the current
equations cannot consistently handle.
