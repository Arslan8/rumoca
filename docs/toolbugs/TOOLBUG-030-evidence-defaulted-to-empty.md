# TOOLBUG-030: solve-domain evidence defaulted to empty

**Status:** fixed 2026-09-25
**Found:** the same sweep as
[TOOLBUG-029](TOOLBUG-029-folding-deleted-functions-from-the-artifact.md); it
was the one in-flight failure with a different cause.

## The defect

`rumoca-eval-solve/src/domain_diagnostics.rs` closed a diagnostic scope with

```rust
let evidence = EVIDENCE.with(|slot| slot.borrow_mut().take().unwrap_or_default());
```

If the slot were ever empty, the report would be emitted with zero faults and
zero unobserved evaluations — reporting *a clean run* for a run whose evidence
had gone missing. The repository already has a gate against exactly this
(`test_eval_solve_has_no_silent_default_value_fallbacks`, which bans
`.unwrap_or_default()` and `.unwrap_or(0.0)` in that crate), and the new file
tripped it.

## Why it matters

This project's output is verdicts. A diagnostic that cannot distinguish "no
faults occurred" from "the record was lost" produces the one failure mode that
is invisible in review: a clean result nobody questions. It is the same shape
as [TOOLBUG-026](TOOLBUG-026-a-stale-binary-decides-the-verdict.md), where a
stale binary reported eleven blocked cases as though they were measurements.

## Fix

State the invariant instead of defaulting past it:

```rust
let evidence = EVIDENCE.with(|slot| {
    slot.borrow_mut()
        .take()
        .expect("a live Scope holds its evidence until finish takes it")
});
```

`start()` fills the slot and refuses to nest; only `finish` or `Drop` clears
it; and `finish` consumes the live `Scope`. So the slot is present whenever
this runs, and if that ever stops being true the run fails loudly rather than
publishing an empty record.
