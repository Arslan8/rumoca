# Divide-by-zero analysis: what the detector must prove

Instructions for verifying the divisor detector. Written after an external
review found **408 false positives** whose common cause was that the detector
reasoned about *symbols occurring in a denominator* rather than about the
*denominator*.

## The question

For every division `N / D`, the detector must decide satisfiability of

```
constraints  AND  branch_path_condition  AND  denominator == 0
```

and classify the result three ways. Two-way classification is the defect:

| Verdict | Meaning | What to do |
|---|---|---|
| `SAT` | an assignment satisfies all three conjuncts | report it, with the witness |
| `UNSAT` | no assignment can | suppress it, and record the proof |
| `UNKNOWN` | neither could be shown | report as **unresolved**, never as confirmed |

A dependency graph is not sufficient. Knowing that `alpha` occurs in a
denominator does not prove that `alpha = 0` makes that denominator zero.

## What the IR must preserve

| | |
|---|---|
| the complete denominator expression tree | not the set of symbols in it |
| `if`, `when`, and conditional-component path conditions | with their polarity |
| assertions and effective parameter bounds | including bounds inherited from the type |
| constant and parameter bindings | so a witness propagates into derived parameters |
| `min`, `max`, `abs`, powers, comparisons, Boolean operators | as operators, not as opaque calls |
| source provenance for generated expressions | so a compiler-introduced division is not blamed on the modeller |

## Simplification and constraint rules

At minimum: constant folding, symbolic algebraic simplification, interval
propagation, equality and inequality solving, branch feasibility, assertion
constraints, and `min`/`max` lower-bound reasoning.

Three worked examples, each a false positive the review found:

```modelica
1 + alpha*(T - T_ref)     // at alpha = 0 this is 1, not zero
max(eps, abs(R))          // at least eps, so it cannot be zero
Vps - Vns                 // the witness is Vps = Vns, not Vps = 0
```

## Assertions

```modelica
assert(D >= Modelica.Constants.eps);
y = x/D;
```

Zero is outside the model's declared domain. Classify as **assert-protected**,
not as an unguarded divide-by-zero.

If a runtime might evaluate the division before producing the assertion
diagnostic, report *that* separately as a robustness concern. It is a different
claim about a different failure.

## Branches

```modelica
if time < startTime then 0
elseif time < startTime + duration then (time - startTime)/duration
else 1
```

The division's path condition is the conjunction

```
time >= startTime  AND  time < startTime + duration
```

At `duration = 0` these cannot both hold, so the division is unreachable and
the site is `UNSAT`. Note the first conjunct comes from the *negated* first
branch: a detector that only reads the branch it is inside will miss it.

Where a guard mentions something the artifact does not determine — a discrete
variable a `when` clause assigns, most often — the verdict is `UNKNOWN`, not
`SAT`.

## Regression cases

False positives, all of which must come back `UNSAT` or `UNKNOWN`:

| Case | Why it is not a defect |
|---|---|
| [complete temperature denominator](../verifiedBugs/false-positives/FINDING-00185.md) | `alpha = 0` leaves 1; an assertion also protects it |
| [ramp duration](../verifiedBugs/false-positives/FINDING-00002.md) | zero duration empties the branch |
| [composite magnetic denominator](../verifiedBugs/false-positives/FINDING-03714.md) | zeroing one operand does not zero the sum |
| [limPID gain](../verifiedBugs/false-positives/FINDING-04783.md) | an assertion, and a positive bound on `Ni` |
| [switched-capacitor guard](../verifiedBugs/groups/switched-capacitor-guard.md) | `max(eps, abs(R))` excludes zero |
| [trapezoid edge](../verifiedBugs/groups/zero-trapezoid-edge.md) | a zero edge duration gives an empty branch interval |

True positives, all of which must come back `SAT` with a witness:

| Case | The witness |
|---|---|
| [equal op-amp rails](../verifiedBugs/confirmed/BUG-024.md) | solve `Vps - Vns = 0`, giving `Vps = Vns` |
| [tank resistance](../verifiedBugs/confirmed/FINDING-05128.md) | direct, unguarded `level/resistance` |
| [machine reactance equality](../verifiedBugs/groups/machine-reactance-equality.md) | two nonzero parameters made equal |

## Acceptance criterion

Every reported finding must contain the **complete denominator**, the **active
path**, the **applicable constraints**, and a **valid zero witness**.

## How to check the current implementation

```console
$ python3 -m pytest packages/modelsan/tests/test_divisor_reasoning.py -q
$ python3 -m pytest packages/modelsan/tests/test_divisor_witness.py -q
$ python3 -m pytest packages/modelsan/tests/test_symbol_contract.py -q
```

Each named case above is one test, referencing the report it refutes. To check
one model by hand:

```console
$ python3 tools/sweep/check_one.py <model> --target <name> --sanitizer divisor
```

The verdict, the interval the denominator was shown to lie in, and the proof or
the witness are all in the printed evidence.
