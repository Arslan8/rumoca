# FINDING-04397: Zero stiffness is a force-free spring limit

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-spring-stiffness |
| Model | Modelica.Mechanics.Rotational.Examples.FirstGrounded |
| Target | spring.c |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-firstgrounded-spring-c-zerolimit.md](../../v2/bugs/FINDING-firstgrounded-spring-c-zerolimit.md) — reviewed as `FINDING-04397-firstgrounded-spring-c.md`, which a later run renamed |
| Original SHA-256 | bca4edcb64fd558440a8fe358acf5b21668b90fa5ac33434f2bedc053108e6f6 |

## Why this is a false positive

The constitutive equation multiplies displacement by c (f=c*(s_rel-s_rel0) or tau=c*(phi_rel-phi_rel0)). At c=0 it transmits no elastic force; there is no reciprocal and the declaration intentionally has min=0. A disconnected or under-constrained surrounding mechanism is topology-specific, not proof that the component bound is defective.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Rotational/Components/Spring.mo:4`. Role: `parameter`; binding: `10000.0`; effective min: `0`; effective max: `None`. 

[Mechanics/Rotational/Components/Spring.mo — source snapshot](../evidence/sources/df63d562c01fc253-Spring.mo)

```modelica
2: model Spring "Linear 1D rotational spring"
3:   extends Modelica.Mechanics.Rotational.Interfaces.PartialCompliant;
4:   parameter SI.RotationalSpringConstant c(final min=0, start=1.0e5)
5:     "Spring constant";
6:   parameter SI.Angle phi_rel0=0 "Unstretched spring angle";
7: 
```

[Mechanics/Rotational/Components/Spring.mo — source snapshot](../evidence/sources/df63d562c01fc253-Spring.mo)

```modelica
2: model Spring "Linear 1D rotational spring"
3:   extends Modelica.Mechanics.Rotational.Interfaces.PartialCompliant;
4:   parameter SI.RotationalSpringConstant c(final min=0, start=1.0e5)
5:     "Spring constant";
6:   parameter SI.Angle phi_rel0=0 "Unstretched spring angle";
7: 
8: equation
9:   tau = c*(phi_rel - phi_rel0);
10:   annotation (
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/078c657a65dbf3e1.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-spring-stiffness.md) · [Index](../README.md)
