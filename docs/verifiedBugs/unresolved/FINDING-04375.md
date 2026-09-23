# FINDING-04375: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | needs-semantic-proof |
| Model | Modelica.Mechanics.Rotational.Examples.CompareBrakingTorque |
| Target | J |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-comparebrakingtorque-j-zerolimit.md](../../v2/bugs/FINDING-comparebrakingtorque-j-zerolimit.md) — reviewed as `FINDING-04375-comparebrakingtorque-j.md`, which a later run renamed |
| Original SHA-256 | 47d2dd7f525813a6a9dc2cc0528e0ed28f2e4c4a61279884f862815f51947390 |

## What remains unresolved

The nominal Rumoca run passes. Available perturbation outcomes are listed below, but no reviewed proof yet connects this exact claim to an unguarded invalid equation or refutes it. A failed post-translation override may change model structure; a passing zero probe alone does not prove the complete parameter domain safe.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Rotational/Examples/CompareBrakingTorque.mo:4`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Mechanics/Rotational/Examples/CompareBrakingTorque.mo — source snapshot](../evidence/sources/4a146eb70f1f35af-CompareBrakingTorque.mo)

```modelica
2: model CompareBrakingTorque "Compare different braking torques"
3:   extends Modelica.Icons.Example;
4:   parameter SI.Inertia J=1 "Moment of inertia";
5:   parameter SI.AngularVelocity w_start=100 "Initial speed of inertia";
6:   parameter SI.Torque tau_nominal=100 "Nominal torque";
7:   parameter SI.AngularVelocity w_nominal=abs(w_start) "Nominal speed";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/fe3161ba002311e0.json). Baseline: **clean**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/needs-semantic-proof.md) · [Index](../README.md)
