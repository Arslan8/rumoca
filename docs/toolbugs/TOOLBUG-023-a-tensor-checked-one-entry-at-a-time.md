# TOOLBUG-023: a tensor checked one entry at a time

| | |
|---|---|
| **Component** | `modelsan.sanitizers.physical`, `modelsan.physical.domains.{mechanical,electrical}` |
| **Severity** | High — 268 reports, and a class of real defect it could not have caught |
| **Found by** | External review of the published reports, 2026-09-17 |
| **Status** | Fixed. Aggregate pass plus component-scoped sign rules; 15 cases in `tests/test_aggregate_and_sign.py`. |

## The defect

Two rules were applied to the wrong subject.

**An inertia tensor is not six scalars.** `MultiBody.Parts.Body` declares
`I_11 … I_32` and assembles them into a symmetric 3×3. The constraint is that
the matrix is positive semidefinite; the off-diagonal entries are signed
products of inertia and the declaration says so with `min = -C.inf`. Checking
each entry against `> 0` reported **182 valid tensors**.

**A resistance is not a component.** `SI.Resistance` is declared by a passive
resistor, by a negative-impedance converter, by a machine winding and by
anything measuring ohms. Keying on the quantity gave all of them `R > 0`, which
contradicts `Basic.Resistor`'s own documentation — "The Resistance R is allowed
to be positive, zero, or negative" — in **65 more reports**, and demanded a
strictly positive stator resistance from machine models that idealise it to
zero in **21 more**.

## The part that is not a false-positive story

A scalar check on an inertia tensor is not merely noisy. It is unsound:

```
[[1, 2, 0],
 [2, 1, 0],
 [0, 0, 1]]
```

Every entry passes `I_11 > 0`, `I_22 > 0`, `I_33 > 0`, and the matrix has an
eigenvalue of −1. The rule that produced 182 false positives would also have
passed a tensor no rigid body can have. **Removing the false positives is what
made the true one reachable**, and this is the third time in this project that
a precision fix also fixed a recall gap.

There is a second trap inside the fix. Sylvester's criterion over the *leading*
principal minors decides positive definiteness, not semidefiniteness:
`[[0,0,0],[0,1,0],[0,0,-1]]` has leading minors 0, 0, 0 and an eigenvalue of
−1. All seven principal minors are checked, and a test pins it.

And a third: for any rigid body each principal moment is at most the sum of the
other two, which is a tempting extra check. `[[2,-1,0],[-1,2,0],[0,0,1]]` has
principal moments 1, 1, 3 and is a tensor the specification requires to
**pass**. Realizability is computed, carried in the diagnostic, and never used
as a verdict.

## The fix

An aggregate pass that groups the six fields by component instance and
declaring class, decides the assembled matrix, emits **at most one** finding
per tensor, and *excludes* its fields from the scalar rule. A tensor declared
only as a 3×3 — `Parts.BodyBox` computes its inertia from the box geometry —
is recognised on its own, because the scalar rule had been comparing a matrix
with zero and reporting `boxBody1.I > 0`, which is not a proposition.

For resistance, three contracts where there had been one, and a third sign
domain: `elec.machine_winding_resistance.non_negative` says `>= 0`, so zero is
the ideal lossless winding and a negative stator resistance is still reported.
Where no declaring class establishes the premise, a violation is an advisory
(`physical-invariant-violated-by-quantity-alone`) rather than a confirmed one.

The design is in
[`../method/aggregate-and-signed-domains.md`](../method/aggregate-and-signed-domains.md).

## Effect

| | before | after |
|---|---:|---:|
| `physical-bound-permits-zero` | 295 | 207 |
| `physical-zero-is-a-supported-limit` | 2973 | 2695 |
| inertia-tensor findings | 278 scalar | 18 undecided, 0 invalid |
| **defect claims** | **2468** | **2371** |

No inertia tensor in the corpus is invalid. The 18 undecided ones are bound to
`resolveDyade1(...)` or to an index into a computed matrix, which this analysis
does not evaluate; their fields are excluded from the scalar rule either way,
because that rule is wrong about products of inertia whether or not the values
are known.

Of the four groups this addressed, three are fully resolved:
`signed-inertia-tensor` (182), `signed-polyphase-element` (63) and
`signed-electrical-element` (2). `signed-machine-data-resistance` keeps 19 of
21 deliberately — the review asked for zero to be allowed and negatives still
reported, and those 19 now claim `>= 0`.

## A precision figure moved a long way, and the reason is not an improvement

`physical-bound-permits-zero` was measured at **2.6%** on 39 draws and is now
**72.5%** on 40. Nothing about the detector got better. The stratum lost its
mass-and-inertia members to the aggregate pass, and what remains is **74%** one
declaration: `Thermal.FluidHeatFlow.Media.Medium.rho`, whose `SI.Density` type
carries `min=0` while `BaseClasses/TwoPort.mo:34` writes
`V_flow = flowPort_a.m_flow/medium.rho`. That is a true positive, and the
stratum is now mostly that one true positive counted 154 times.

Four of its eleven sampled declarations are true positives. **Both numbers are
in [`../findings/precision.md`](../findings/precision.md)**, because the
finding-level figure and the declaration-level figure answer different
questions and only one of them is about the library.
