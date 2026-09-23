# TOOLBUG-014: array equation families are absent from the bitcode

| | |
|---|---|
| **Component** | Rumoca, `crates/rumoca-bitcode/src/export.rs` |
| **Severity** | High — the artifact under-reports the equation system |
| **Status** | Fixed — export, import, textual IR, disassembler and SDK |

## What is missing

`export_equations` enumerates only scalar equations:

```rust
let count = match kind {
    EquationKind::Continuous => view.continuous_equation_count(),
    EquationKind::Initial => view.initialization_equation_count(),
};
```

The DAE also holds **structured equation families** — the compact form of an
array or `for` equation, counted by `view.continuous_family_count()`. Nothing
exports them, and nothing records that they were left out.

## Demonstration

```modelica
model Arr
  Real x[3];
equation
  for i in 1:3 loop
    x[i] = i;
  end for;
end Arr;
```

```
variables:        [('x', 3)]        -> 3 scalar unknowns
equations in RBC:  0
```

Three unknowns, no equations. The artifact describes a model that determines
nothing, and validates cleanly.

## Scale

`Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Transformer`:

```
934 scalar unknowns
829 variable nodes
715 continuous equations exported
```

100 of its 1262 variables are arrays. The balance the compiler enforces at DAE
construction does not hold in the exported artifact, because roughly 219
equations' worth of families never made the trip.

## Why it matters beyond a count

Any consumer reasoning about solvability is reading an incomplete system.
`StructureSan`'s equation-variable matching reported **1233 findings over 119
models** — under-constrained regions that are nothing of the sort; the
equations exist, they are simply not in the file. The models most affected are
the ones most worth analysing: machines, polyphase converters, multibody.

It is also invisible. An `Unsupported` expression node announces itself; a
missing equation family does not, and the summary counts agree with the
truncated list.

## How it was found

By the contradiction between two things I had established separately: Rumoca
*refuses* to construct a DAE from an unbalanced model, so a matching over a
successfully compiled model should not find hundreds of unmatched unknowns.
When it did, the artifact was the thing to doubt.

## Fix

`RbcEquationFamily` carries the bodies, the iteration `extents`, the
`scalar_view`, and — the field a balance or matching analysis actually needs —
`scalar_rows`, the number of scalar equations the family stands for. The
summary counts both families and rows, because a consumer walking the artifact
wants the first and a consumer counting equations wants the second.

Kept compact rather than expanded to scalar rows: expanding multiplies the
artifact by the array extent and loses the fact that the rows share one source
equation.

```
Arr (Real x[3], for i in 1:3)
  scalar equations : 0
  equation families: 1   rows=3 extents=[3] view=binder_substitution
  -> 3 scalar unknowns, 3 equations accounted for
```

`IMC_Transformer`, the worst case found:

```
                        before   after
scalar equations          715      715
family rows                 0      198
continuous unknowns       913      913
balance                  -198       +0
```

## The round trip needed five more things

Carrying `scalar_rows` fixed the *count*. Rebuilding the family needed the rest,
and each one was found by the next import failure after the previous fix:

| What was missing | Symptom |
|---|---|
| `RbcDomain` — the iteration domain, its binders and their affine bounds | import refused outright: a DAE rebuilt without it would silently be missing the rows |
| `RbcCoordinate::Binder` | `coordinate kind not in bitcode v1` — the `i` in `x[i] = i` |
| `RbcExprNode::Index` and the other array/record forms | `expression form not in bitcode v1` — `x[i]` itself |
| `RbcType.record` | `invalid expression arity: expected 0, found 2`; a record type exported as a field-free `String`, so `Complex` and everything built on it was unimportable |
| `RbcEquationFamily.reads` | see below |

Until domains were carried, import refused rather than dropping, because
dropping would have recreated the same bug one layer down: a DAE rebuilt from a
*complete* artifact would quietly be missing equations and would still validate.
It now rebuilds:

```
$ rumoca bitcode round-trip Arr.rbc
Arr.rbc: round-trip preserves every compared field
```

## The incidence set, and a false positive it caused

`RbcEquation` carries a `reads` set computed by the compiler's own scalar
coordinate projection. Families did not, so a consumer had to walk the symbolic
body instead — and an expression walk misses array and record *selections*.

On `Modelica.Mechanics.MultiBody.Examples.Elementary.DoublePendulum`, a model
with 255 families and 1245 scalar unknowns, the missing edge produced exactly
one unmatched unknown and one unmatched equation:

```
VAR revolute2.constantTorque.flange.phi   1 scalar, 0 determined
EQ  102  revolute2.tau = -(revolute2.frame_b.t * revolute2.e)
```

A `STRUCTURAL_MATCH_FAILURE` reported against a model that has none. With
`reads` exported from the same projection the scalar equations use, the model
matches 1245 of 1245 and the finding disappears. The rule this confirms: a
*missing* incidence edge is indistinguishable from a real defect, so incidence
must never be re-derived by the consumer.

## Consumers

`StructureSan` no longer skips array models. Its matching is now a maximum
*flow*: a variable node has capacity `scalar_count`, an equation node capacity
`scalar_rows`, and a scalar equation is the capacity-1 special case, so an
all-scalar model behaves exactly as before. A one-to-one matching cannot express
"one family of six rows determines two arrays of three".

The shared expression traversal (`modelsan.dae.traversal.walk_expressions`) now
descends into family bodies. Until it did, *every* expression inside a `for`
loop — every division, every unit, every bound — was invisible to every pass
built on it, not just to the matching.
