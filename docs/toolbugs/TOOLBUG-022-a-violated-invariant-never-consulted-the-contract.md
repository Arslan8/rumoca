# TOOLBUG-022: the contract was consulted for missing bounds, not for violated ones

| | |
|---|---|
| **Component** | `modelsan.sanitizers.physical.PhysicalSan.analyze` |
| **Severity** | Medium — it kept the highest-precision stratum's worst members |
| **Found by** | Cross-checking the sanitizers against the external review in `docs/verifiedBugs/`, 2026-09-16 |
| **Status** | Fixed. The zero contract now gates both paths. |

## The defect

[TOOLBUG-020](TOOLBUG-020-zero-behaviour-was-decided-three-times.md) gave the
three detectors one classification of what zero means for a parameter.
PhysicalSan consulted it in the loop over declarations that *permit* a
forbidden value, and not in the loop over declarations that already *hold* one.

So `CoreParameters.GcRef`, which ships at zero because

```modelica
final parameter SI.Conductance GcRef = if PRef <= 0 then 0 else PRef/VRef^2/m
```

with `PRef(min=0) = 0`, was reported as `physical-invariant-violated` — the
stratum measured at **100% precision** on 30 draws. The contract that says zero
is how this library disables core losses was computed, and then not asked.

The external review found the same thing independently and filed 120 instances
under the group `disabled-core-loss`.

## The fix

The violation path now asks the same contract, and only about zero:

```python
supported = (contracts.zero_is_safe(variable.id)
             if variable is not None and violation.observed == 0.0
             else None)
```

**A zero contract excuses zero and nothing else.** A negative inductance is not
made acceptable by a component documenting that zero is an ideal short, and the
guard on `violation.observed == 0.0` is what keeps the two apart.

## Two ways the same parameter escaped

`GcRef` needed two separate pieces of evidence, because the default run folds
parameter bindings before the sanitizers see them:

- with `--keep-parameter-chains` the binding survives, and
  `infer.declared_value_contract` reads it: a binding that evaluates to zero,
  or a conditional with a literal zero branch, is the declaration naming zero
  as one of its intended values;
- in the default run the binding is already a number, and only the catalogue
  can say what the number meant.

Both are `DECLARED`, never `PROVEN`: they record what the library says.

## Effect

`physical-invariant-violated` loses its `GcRef` members. The stratum's measured
precision does not change — the 30 adjudicated draws were all true positives
and none of them was a `GcRef` — but the population it is measured over is now
the one the sample was drawn from.

Of the external review's 3304 false positives, **2735 (83%)** are now either
not reported at all or reported only under a kind that makes no defect claim.
The 569 that remain are listed by group in
[`../findings/precision.md`](../findings/precision.md) and are the next thing
to work on.
