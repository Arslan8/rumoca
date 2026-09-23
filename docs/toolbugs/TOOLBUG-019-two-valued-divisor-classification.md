# TOOLBUG-019: the divisor analysis had no way to say "I don't know"

| | |
|---|---|
| **Component** | `packages/modelsan/modelsan/divisor/` |
| **Severity** | Medium — a false-positive class, and a missing honesty |
| **Found by** | Independent review of the published reports, 2026-09-16 |
| **Status** | Fixed. Three-valued classification; 9 regression cases in `tests/test_divisor_reasoning.py`. |

## The defect

The detector answered a satisfiability question — `constraints AND path AND
denominator == 0` — with two outcomes: it found an assignment, or it did not.
A site whose *path* it could not decide was treated as reachable and reported
as a defect.

`Trapezoid` divides by `rising` inside `time < T_start + T_rising`, where
`T_start` is a discrete variable a `when` clause assigns. At `rising = 0` the
branch is empty **if** `T_start >= startTime`, which is true of the model and
is not deducible from the artifact. Reporting it claimed a defect that is not
there; suppressing it would have hidden one that might be.

## Three answers, not two

| Verdict | Meaning | Action |
|---|---|---|
| `SAT` | an assignment satisfies all three conjuncts | report, with the witness |
| `UNSAT` | no assignment can | suppress, and record the proof |
| `UNKNOWN` | neither could be shown | report as **unresolved**, never confirmed |

Over the corpus: **5081 divisions, 2896 UNSAT, 1553 SAT, 632 UNKNOWN.** 57% of
all divisions are now *proved* safe rather than merely not reported, and the
count is recorded per model in the run under `divisions` — a suppressed finding
leaves no trace otherwise, and that count is the denominator a precision figure
needs.

## What the reasoning had to gain

Four capabilities, each demanded by a specific case:

**Interval propagation with `min`/`max` lower bounds.** MSL holds a denominator
away from zero by writing `max(eps*oneOhm, abs(R))`. Propagating ranges through
`max` and `abs` proves the interval is `[2.2e-16, inf)`, which excludes zero —
45 reports withdrawn with a proof rather than by a tolerance accident.

**De Morgan over path conditions.** `Trapezoid` writes its "before the signal
starts" case as `if A or B or C then 0 else ...`. Taking the *false* side of a
disjunction implies all three negations; taking the true side of a conjunction
implies both conjuncts. The other two combinations imply nothing definite and
are dropped. Without this the guard contributed no bound at all.

**Folding derived parameter bindings.** `T_rising = rising` must become zero
when `rising` does, or the branch guarded by it cannot be evaluated. The witness
now propagates through parameter bindings, not just through equations.

**Suppressing the uninteresting UNSAT.** Emitting one finding per provably-safe
division produced 2660 lines saying nothing is wrong. A denominator that simply
cannot be zero is suppressed; one the model *actively guards* — by an assertion
or a branch — is still reported, because the guard is a design decision a reader
may want to challenge.

## A defect found while fixing it

`VariableRef.kind` is the *coordinate* kind — `"parameter"`, `"algebraic"`,
`"state"` — not a `"value"`/`"derivative"` tag. The interval evaluator tested it
against `"value"`, so it rejected every plain variable reference, every interval
widened to unknown, and no UNSAT proof was ever found. The `max(eps, abs(R))`
family was being suppressed by a tolerance coincidence rather than by the
reasoning written for it.

## Regression cases

`packages/modelsan/tests/test_divisor_reasoning.py` holds one test per case the
review named, six requiring `UNSAT` or `UNKNOWN` and three requiring `SAT` with
a witness, plus a test that every reported defect carries the four required
parts: the complete denominator, the active path, the applicable constraints,
and a valid zero witness.

The instructions this work was checked against are in
[`../method/divide-by-zero-analysis.md`](../method/divide-by-zero-analysis.md).
