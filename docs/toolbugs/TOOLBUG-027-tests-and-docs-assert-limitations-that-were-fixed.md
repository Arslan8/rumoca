# TOOLBUG-027: tests and docs assert limitations that were already fixed

**Status:** open
**Found:** 2026-09-24, verifying the MSL known-issues campaign and test suite.

## The defect

Three records in the tree assert a capability gap that no longer exists. Each
was true when written. Nothing re-checks them, so they persist as evidence
against our own tool.

### 1. Clocked import is claimed unsupported

`packages/modelsan/tests/test_solver_diagnostics.py::
test_unsupported_clocked_import_is_not_a_model_bug` asserts that a model using
`sample` / `when` / `pre` yields `ExecutionStatus.BACKEND_ERROR`. It now yields
`SUCCESS`, and the result is *numerically correct*, not a silent no-op:

```
d: 0.11=1.0  0.22=2.0  0.33=3.0  0.44=4.0  0.55=5.0     (5 events, 5 sample points)
x(0.55) = 1.2500000000000044     hand-computed 0.1*(1+2+3+4) + 0.05*5 = 1.25
```

The test is the only thing still failing in the suite, and it fails by being
right about 2026 and wrong about today.

### 2. Native MoistAir is claimed blocked

`docs/evaluations/msl-upstream-open-issues-2026-09-24/detection-followup.md:82`
states "Native MoistAir still stops with EF015 ... no native detection is
claimed", and `detection-native.json` records both MoistAir cases as `blocked`.
Re-running the campaign against the current binary gives
`MoistAirReduced -> model-rejected` with the specific finding
`solver / compile-time-array-bounds / high`, "index 2, size 1" at
`MoistAir.mo:1273` — which is exactly upstream issue #4771 — and
`MoistAirFull -> no-violation-observed`, a clean control.

Native detection is **6/6 with 5 clean controls**, not the documented 5/6.

### 3. The machine-readable census contradicts the prose

`assessment.json` records `demonstrated_modelsan_detection: false` for all 353
entries, including the six that demonstrably work. `build_index.py` renders the
published index from that file, so the index understates the result.

## Why it matters

All three understate the tool. That is the less dangerous direction, but it is
the same mechanism that would overstate it: a recorded claim with no owner and
no re-check. An evaluation document that is stale in our favour is still an
evaluation document we cannot cite.

## Fix

- Replace the clocked test's limitation assertion with the behavioural one
  above (step times, event count, and the closed-form integral).
- Re-run the campaign and regenerate `detection-native.json`; correct the
  "Remaining coverage gaps" paragraph.
- Backfill `demonstrated_modelsan_detection` for the six, and have
  `build_index.py` fail when the flag disagrees with `detection-*.json`.

Related: [TOOLBUG-026](TOOLBUG-026-a-stale-binary-decides-the-verdict.md), which
is why instance 2 was recorded wrong in the first place.
