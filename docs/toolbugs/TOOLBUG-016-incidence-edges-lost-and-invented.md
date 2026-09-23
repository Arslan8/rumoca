# TOOLBUG-016: four ways the equation–variable incidence was wrong

| | |
|---|---|
| **Component** | `rumoca-bitcode` export, and `modelsan.analysis.structure` |
| **Severity** | High — every one of them produced `STRUCTURAL_MATCH_FAILURE` findings against models the compiler had already proved balanced |
| **Status** | Fixed. Corpus findings: **1324 → 63**, models with findings **166 → 24**. |

## Why a matching failure is a self-checking claim

Rumoca refuses to build a DAE from an unbalanced model. So on any model that
compiled, the equation and unknown counts agree by construction. If a matching
over that model still fails, one of two things is true: the model is
structurally singular despite balancing, or **the graph is wrong**. The second
is far more likely, and it was, four times.

Each fix was found the same way: take the min cut of the failed flow, read the
witness set, and ask which edge it is missing.

## 1. Array equations counted as one

An equation family stands for `scalar_rows` equations and an array variable for
`scalar_count` unknowns, but both arrive as a single object. A one-to-one
matching cannot even express "one family of six rows determines two arrays of
three". The matching is now a maximum *flow* with a capacity per node; a scalar
equation is the capacity-1 case, so an all-scalar model behaves exactly as
before.

See [TOOLBUG-014](TOOLBUG-014-structured-equations-not-exported.md), which is
where the families came from in the first place.

## 2. A family's incidence projected for one row only

`RbcEquationFamily.reads` was computed by projecting the symbolic body *once*,
with no domain point. The projection then reports the coordinates of the first
row and no other: on `IMC_Transformer`, 38 of 76 families lost `pin[2]` and
`pin[3]`.

The fix walks the rows the way `rumoca-phase-structural` already does —
`domain.structured().index_tuple_at(point)` for each point, `scalar_view()
.body_scalar(...)` for the row's scalar index. Disagreeing with the compiler's
own incidence was the bug.

```
IMC_Transformer   913 unknowns, 913 rows
  before:  890 matched, 23 phantom failures
  after:   913 matched, 0
```

## 3. A whole equation partition was never exported

MLS Appendix B.1b **coupled discrete-Real equations** determine the
discrete-Real unknowns — a sampled hold, a mean held between events. They live
in their own DAE partition and nothing exported them. The artifact was short
exactly one equation per discrete-Real variable, so a consumer that also
excluded those variables (correctly, since nothing appeared to determine them)
saw a system with more constraints than unknowns:

```
AnalysatorAC   301 unknowns, 320 rows   ->   19 phantom UNMATCHED_EQUATION
               (and exactly 19 discrete-Real variables)
```

`RbcDiscreteRealEquation` and `RbcInitialDiscreteValue` now carry it, import
rebuilds it through `construction.discrete(...)`, and the summary counts it
separately from `equations` — merging the two counts would make every model
with a `sample` look over-constrained.

## 4. `pre(v)` was an incidence edge, and `der(x)` was not

These are the same mistake twice, in opposite directions.

`pre(v)` (MLS §3.7.5) is the value `v` held at event entry — a **known**. An
equation reading it depends on `v` but cannot determine it. Folded into
`reads`, the B.1b equation

```
meanCurrent.y_last = if not yGreaterOrEqualZero then f * pre(x) else max(0, f * pre(x))
```

looked able to determine the state `x`. The flow spent it there, and `y_last`
came out unmatched. `reads_previous` now carries these separately — a
dependency analysis unions the sets, a matching analysis does not.

`der(x)` is the opposite: the equation containing it **is** the one that
determines the state `x`. It was already separate, in `reads_derivative`, and
the matching ignored it — so a state appearing only as `der(x)` fell out of the
graph entirely. Three of them in `AnalysatorDC`.

```
ModelicaTest.Translational.Vehicles   678 unknowns
  before:  660 matched
  after:   678 matched, 0 findings
```

## Also: the state check saw only scalar equations

`STATE_WITHOUT_DERIVATIVE_CONSTRAINT` walked `model.equations` and nothing else,
so a state whose `der()` sits inside a `for` loop or a `when` looked
unconstrained: **246 findings across 41 models**, `imc.airGap.psi_ms` among
them. It now walks every partition that can carry `der(x)`. All 246 were false.

## Where it landed

| | models with findings | findings |
|---|---:|---:|
| families counted (fix 1 only) | 166 | 1324 |
| + per-row family incidence (2) | 163 | 717 |
| + B.1b partition, state fix (3) | 134 | 626 |
| + `pre`/`der` incidence (4) | **24** | **63** |

333 of 848 corpus models reach the analysis; 309 of them report nothing.

## What the remaining 63 are

**22 of the 24 models are sub-circuit building blocks compiled standalone** —
`.OpAmpCircuits.*`, `.Examples.Utilities.*`, `.Components.*`. These are meant to
be instantiated inside a larger circuit. Compiled on their own, their interface
connectors are unconnected, which contributes a `flow = 0` equation without a
matching potential unknown, and the result is a system that balances by count
and is structurally singular anyway. That is a correct structural result, and
not a defect in MSL.

The other two are real runnable examples —
`Modelica.Clocked.Examples.Elementary.RealSignals.AssignClockVectorized` and
`.SampleVectorizedAndClocked`, one and two findings. Both are clocked, and
clocked coordinates (`clock_interval`, `previous`) are among the kinds the
schema still does not carry
([TOOLBUG-015](TOOLBUG-015-function-bodies-not-carried.md)), so these are not
yet adjudicable either way and are **not** claimed as findings.

## The rule this leaves behind

A missing incidence edge and a real defect are indistinguishable in the output.
So incidence is never re-derived by a consumer: it comes from the compiler's own
scalar-coordinate projection, over every row, split by *how* the variable is
read — current value, derivative, left limit — because those three answer
different questions and a consumer that flattens them gets the wrong answer.
