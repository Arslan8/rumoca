# FINDING-04418: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | needs-semantic-proof |
| Model | Modelica.Mechanics.Translational.Examples.CompareBrakingForce |
| Target | m |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-comparebrakingforce-m-zerolimit.md](../../v2/bugs/FINDING-comparebrakingforce-m-zerolimit.md) — reviewed as `FINDING-04418-comparebrakingforce-m.md`, which a later run renamed |
| Original SHA-256 | 9bee7597b293749ccdcd4e5ded002960c5f755277e76851e3f6c2e0dfee3a396 |

## What remains unresolved

The nominal Rumoca run passes. Available perturbation outcomes are listed below, but no reviewed proof yet connects this exact claim to an unguarded invalid equation or refutes it. A failed post-translation override may change model structure; a passing zero probe alone does not prove the complete parameter domain safe.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Translational/Examples/CompareBrakingForce.mo:4`. Role: `parameter`; binding: `1`; effective min: `0`; effective max: `None`. 

[Mechanics/Translational/Examples/CompareBrakingForce.mo — source snapshot](../evidence/sources/46d5f21a0434641a-CompareBrakingForce.mo)

```modelica
2: model CompareBrakingForce "Compare different braking forces"
3:   extends Modelica.Icons.Example;
4:   parameter SI.Mass m=1 "Mass";
5:   parameter SI.Velocity v_start=100 "Initial speed of mass";
6:   parameter SI.Force f_nominal=100 "Nominal force";
7:   parameter SI.Velocity v_nominal=abs(v_start) "Nominal speed";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/a87b7cf9305a618d.json). Baseline: **clean**.

| Probe | Outcome |
|---|---|
| `m=0` | reported-failure |

Diagnostic: solve-IR evaluation failed: algebraic projection did not converge at event boundary: worst scaled residual row=34 target=mass4.a value=1.000000e2 ratio=1.000000e12 norm=1.000000e2 row_scale=1.000000e0 scaled_tolerance=1.000000e-10

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/needs-semantic-proof.md) · [Index](../README.md)
