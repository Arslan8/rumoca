> Historical preliminary record. GitHub access and the census are now complete; access-status statements below are superseded by [the current evaluation](README.md) and [focused results](focused-results.md). Existing execution evidence remains historical evidence, not a fresh run.

# Initial upstream review: four issues

Review date: 2026-09-24. This is a bounded assessment of upstream issues #4801,
#4794, #4773, and #4770, **not a complete inventory or a detection experiment**.
Three issue bodies were readable; #4801 was not. No reproducer was executed and
no issue is counted as detected. Machine-readable evidence is in
[review-initial.json](review-initial.json).

## Results

| Upstream issue | Evidence read | Assessment | Current numerical sanitizer | Missing evaluation capability |
|---|---|---|---|---|
| [#4801 — SupportFriction interpolation smoothness](https://github.com/modelica/ModelicaStandardLibrary/issues/4801) | Listing title and open state only; body unavailable | **Unclassified**; neither confirmed bug nor dismissed | Unknown for the actual report | Retrieve body, discussion, and reproducer before choosing an oracle |
| [#4794 — temporaryFileName / tmpnam](https://github.com/modelica/ModelicaStandardLibrary/issues/4794) | Body and metadata; linked PR unavailable | Security/API-hardening report; local implementation contains the reported mechanism | Not a numerical-domain detector target | C/external-function security checks plus atomicity and filesystem tests |
| [#4773 — Windows file-path encoding](https://github.com/modelica/ModelicaStandardLibrary/issues/4773) | Body and metadata; discussion not available | Reported platform/interface defect; local implementation contains relevant code | Not a numerical-domain detector target | Windows UTF-8 path roundtrip tests and external-call tracing |
| [#4770 — Spline interpolation of Blocks.Tables](https://github.com/modelica/ModelicaStandardLibrary/issues/4770) | Body and metadata; attachment unavailable | Open **Feature**, labeled **worksforme**; not established as a bug | No same-interpolation derivative correctness oracle | Obtain reproducer; interpolation-aware derivative and continuity contracts |

The open states above are from cached GitHub pages, not a fresh authenticated
API snapshot. An open issue is not automatically a confirmed bug. Missing
comments mean this review cannot claim to have read the complete discussion.

## #4801: assessment blocked by missing report

The accessible [upstream listing](https://github.com/modelica/ModelicaStandardLibrary/issues)
names a SupportFriction smoothness issue opened on 2026-08-25. Direct fetch,
navigation from that listing, and a query-URL variant did not retrieve its body.
No statement about the reporter's intended behavior or trigger is justified yet.

Local MSL 4.1.0 does have the named component. Its `smoothness` parameter is
passed to `ExternalCombiTable1D`, and its calls distinguish constant, linear,
and other interpolation modes. See local `SupportFriction.mo` lines 11, 24–31,
41–43, and 65–68 (file path and digest in JSON). This **does not prove** the
reported problem applies to 4.1.0 or is already fixed there.

If the body eventually establishes an unintended loss of smoothness, the useful
oracle would test the promised continuity order around interpolation knots,
separately from intentional stick/slip transitions. This is a **conditional
test proposal**, not a classification of the unread report. Do not equate every
friction discontinuity with an error.

## #4794: outside numerical sanitizer scope

The [report](https://github.com/modelica/ModelicaStandardLibrary/issues/4794)
asks to replace temporary-name generation with an atomic creation API and
explicitly raises backward-compatibility questions. The linked PR #4795 was
not readable, so its solution or merge status is not assumed.

Local `Resources/C-Sources/ModelicaInternal.c` lines 747–760 calls `tmpnam(NULL)`
and returns a copied path. Source inspection therefore confirms this mechanism
exists in the pinned MSL 4.1.0 source; it does **not** constitute an executed
security exploit or a ModelSan detection. The local comment promises a filename
that does not exist, so silently switching to file creation needs an explicit
API-contract decision.

The suitable checks are external-C API linting and a filesystem harness that
tests exclusive creation, concurrent callers, permissions, temp-directory
handling, and the agreed return-value/lifetime semantics. Run in an isolated
temporary directory with benign collision controls. Scalar range/domain checks
cannot establish atomicity. Merely getting a linker warning, or failing to load
an external function, is not a sanitizer hit on this issue.

## #4773: platform-specific contract testing needed

The [report](https://github.com/modelica/ModelicaStandardLibrary/issues/4773)
concerns the UTF-8 external-C string contract versus Windows pathname APIs,
including both input and output paths. It separately notes vendor-side
`loadResource` behavior; that is not evidence of an MSL-only failure.

Local `ModelicaInternal.c` calls `remove(file)` directly at line 488, opens
directories at line 568, and copies directory-entry bytes into Modelica strings
at lines 588 and 603. The relevant implementation pattern is present, but the
actual effect depends on the Windows runtime, code-page configuration, and
external-library build. No Windows execution was performed here.

Use a Windows test matrix with ASCII controls and UTF-8 names outside the active
legacy code page. Create, list, open, rename, and delete the same paths; assert
byte-correct UTF-8 roundtrips and file identity. Record the tool/runtime encoding
and separate an MSL external-C failure from a compiler/vendor conversion error.
This needs platform CI and an I/O/string oracle, not a stronger divide-by-zero
rule. A Linux success would not disprove the Windows report.

## #4770: do not manufacture a false positive from different splines

The [issue body and metadata](https://github.com/modelica/ModelicaStandardLibrary/issues/4770)
describe a derivative comparison between CombiTable1Ds and MATLAB-derived
spline coefficients. The page is marked Feature and worksforme. The attachment
`Splines.zip` and any explanatory discussion were unavailable; the reason for
the label is therefore unknown. This is **not established ground truth for a
defect**, and the label alone is not proof that every underlying claim is false.

Local `Blocks/Tables.mo` lines 144–147 explicitly exempt constant interpolation
from derivative support and linear interpolation from second-derivative support.
Lines 1148–1218 bind table derivatives to external C functions. `Blocks/Types.mo`
lines 6–18 distinguishes Akima, modified Akima, Fritsch-Butland, Steffen, constant,
and linear interpolation. Comparing two different spline families can produce
different derivatives without either implementation being wrong.

First recover the input data and chosen modes. Compare each derivative against
the **same interpolant**, using analytic checks on simple tables and convergent
finite differences away from knots. At knots test only the continuity order
promised for that mode; first-derivative continuity does not promise continuous
second derivatives. Carry interpolation identity, mode, and derivative order
in the analysis contract. Keep controls for intentional linear slope changes
and constant jumps. An external-function/compiler error is a capability blocker,
not evidence of the reported interpolation defect.

## What the current code actually provides

- [DomainSan](../../../packages/modelsan/modelsan/sanitizers/domain.py) `sites()`
  recognizes division, logarithms, square root, and inverse-trigonometric
  domains. It does not inspect filesystem races or finite derivative accuracy.
- [DiscontinuitySan](../../../packages/modelsan/modelsan/sanitizers/discontinuity.py)
  finds parameter-versus-literal conditional thresholds and produces coverage
  information and probe hints. It is not a general smoothness checker.
- [EventSan](../../../packages/modelsan/modelsan/sanitizers/event.py) checks
  timestamp spacing/density. Chattering can be a symptom, not proof that an
  interpolation implementation violated its contract.
- [DifferentialSan](../../../packages/modelsan/modelsan/sanitizers/differential.py)
  can flag disagreements, not attribute them automatically to MSL.
  Its current [trace comparison](../../../packages/modelsan/modelsan/sanitizers/comparison.py)
  pairs values by index; align timestamps and the mathematical interpolant
  before using it for a derivative-accuracy experiment.

## Scoring and priority

All four entries have `test_status = not-executed` and `detected = false`.
Here, false means **no demonstrated detection**, not that an executed detector
missed a proven bug. Do not calculate recall from these four rows.

Retrieve complete issue evidence first. For numerical-sanitizer development,
interpolation/derivative contracts are a plausible new capability, conditional
on a real in-scope defect being established. Windows path correctness and
temporary-file atomicity belong in external-function/platform validation rather
than the numerical detector's recall denominator. Keep separate outcomes for
unread report, feature/question, version-inapplicable issue, platform/compile
blocker, executed symptom, and operation/contract-specific reproduction.
