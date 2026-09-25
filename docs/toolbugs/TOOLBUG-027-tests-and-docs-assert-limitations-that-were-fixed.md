# TOOLBUG-027: tests and docs assert limitations that were already fixed

**Status:** fixed 2026-09-25
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

### 2. Native MoistAir is claimed blocked — RETRACTED

**This entry was wrong.** It read:

> `detection-followup.md:82` states "Native MoistAir still stops with EF015 ...
> no native detection is claimed" ... Native detection is 6/6 with 5 clean
> controls, not the documented 5/6.

That was measured on 2026-09-24 and does not reproduce. Re-running the campaign
on 2026-09-25 gives `MoistAirFull` and `MoistAirReduced` both `blocked`, so
native detection is **5/6 with 4 clean controls** — exactly what the document
claimed. Compiling the model directly reproduces it independently of any
sanitizer, and it reproduces equally with the in-flight flatten work reverted
to its authored state, so neither the pruning-order nor the folding-scope fix
is responsible.

What *is* stale is the blocker's identity: it was EF015, missing record
metadata, and is now ED019, an unsupported function shape proof. The document
now says so.

The lesson is the one this file is about, turned around: a single measurement
is not a fact. The 6/6 claim was taken from one campaign run and repeated in
three places before anything re-ran it, which is exactly the failure mode
[TOOLBUG-026](TOOLBUG-026-a-stale-binary-decides-the-verdict.md) describes.

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
  above (step times, event count, and the closed-form integral). **Done** —
  `test_a_clocked_sample_model_runs_and_integrates_its_discrete_state`.
- Re-run the campaign and regenerate `detection-native.json`; correct the
  "Remaining coverage gaps" paragraph. **Done** — the report is regenerated and
  the paragraph names ED019.
- Backfill `demonstrated_modelsan_detection`. **Done** — set for the five
  issues the regenerated report shows as violated (#3624, #4451, #4459, #4749,
  #4750), read from the report rather than listed by hand so the flag cannot
  drift from the evidence.

Related: [TOOLBUG-026](TOOLBUG-026-a-stale-binary-decides-the-verdict.md), which
is why instance 2 was recorded wrong in the first place.
