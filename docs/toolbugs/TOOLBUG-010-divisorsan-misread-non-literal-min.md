# TOOLBUG-010: DivisorSan read a non-literal `min` as no bound at all

| | |
|---|---|
| **Component** | ModelSan, `sanitizers/divisor.py` |
| **Severity** | High — it manufactured findings against correct models |
| **Status** | Fixed, 2026-09-14, with the corpus re-run |

## What went wrong

`DivisorSan.zero_permitted` asks whether anything on the path to a denominator
excludes zero. It read the declared bound with:

```python
def _literal(expression):
    return getattr(expression, "value", None) if expression is not None else None
```

That reads a bare literal and nothing else. A bound written as a named constant
came back as `None`, which the sanitizer takes to mean *no bound declared*:

```modelica
parameter SI.Length s_ref(min=Modelica.Constants.eps) = 1;   // read as unbounded
parameter SI.Time    T(min=Modelica.Constants.small);        // read as unbounded
```

Both declarations already forbid zero. The sanitizer proposed zero anyway, both
tools failed on the out-of-range override, and the cross-confirmation stage
agreed — because the confirmer asks *does the trigger reproduce in the other
tool*, not *was the trigger legal in the first place*.

## What it cost

Two of the 28 execution-confirmed results were not model defects:

| Reported | Actually declares | Verdict |
|---|---|---|
| `Translational.Components.ElastoGap.s_ref = 0` | `min=Modelica.Constants.eps` | model is correct |
| `Blocks.Continuous.PI.T = 0` | `min=Modelica.Constants.small` | model is correct |

Both were on their way into `docs/verified bugs/` as new findings. They were
caught only by reading the MSL source before writing the file, which is the step
that should not be the last line of defence.

`Modelica.Magnetic.FluxTubes.Examples.Utilities.TranslatoryArmatureAndStopper`
appeared twice more with `stopper_xMax.s_ref` and `stopper_xMin.s_ref`; both are
`ElastoGap` instances and fall with it.

## Why cross-confirmation did not catch it

Worth stating plainly, because the pipeline was built to make findings
defensible and this passed through it. Cross-confirmation establishes that a
failure is a property of the *model* rather than of one tool. It says nothing
about whether the value was one the model ever promised to accept. Two tools
agreeing that `s_ref = 0` breaks `ElastoGap` is correct and uninteresting: the
declaration says `s_ref >= eps`.

The missing check is **admissibility of the trigger**, and it belongs before
confirmation, not after.

## Fix

`_literal` now uses the folding evaluator, which resolves a reference to another
parameter or constant through its binding:

```python
def _literal(expression):
    return constant_value(expression)
```

`Modelica.Constants.eps` is a constant with a binding, so it folds to `2.2e-16`
and `zero_permitted` is correctly `False`.

## What the same bug implies elsewhere

Any sanitizer reading a declared bound with a naive literal reader has this
defect. `PhysicalSan` had the analogous problem and was fixed the same day
(see `docs/architecture/physical-sanitizers.md`), where the symptom was the
reverse: it *failed to report* a violation whose value was written as an
expression.

## Regression

`packages/modelsan/tests/test_divisor.py` — a divisor whose parameter declares
`min=Modelica.Constants.eps` must produce no finding.
