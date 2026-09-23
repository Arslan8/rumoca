# FINDING-04455: Zero stiffness is a force-free spring limit

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-spring-stiffness |
| Model | Modelica.Mechanics.Translational.Examples.InitialConditions |
| Target | s2.c |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-initialconditions-s2-c-zerolimit.md](../../v2/bugs/FINDING-initialconditions-s2-c-zerolimit.md) — reviewed as `FINDING-04455-initialconditions-s2-c.md`, which a later run renamed |
| Original SHA-256 | 58c87036c273506c94c3e322368aa719bef95416586a048ff065c3dce719a571 |

## Why this is a false positive

The constitutive equation multiplies displacement by c (f=c*(s_rel-s_rel0) or tau=c*(phi_rel-phi_rel0)). At c=0 it transmits no elastic force; there is no reciprocal and the declaration intentionally has min=0. A disconnected or under-constrained surrounding mechanism is topology-specific, not proof that the component bound is defective.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Translational/Components/Spring.mo:4`. Role: `parameter`; binding: `1000.0`; effective min: `0`; effective max: `None`. 

[Mechanics/Translational/Components/Spring.mo — source snapshot](../evidence/sources/761ca23f5d4162a3-Spring.mo)

```modelica
2: model Spring "Linear 1D translational spring"
3:   extends Translational.Interfaces.PartialCompliant;
4:   parameter SI.TranslationalSpringConstant c(final min=0, start=1)
5:     "Spring constant";
6:   parameter SI.Distance s_rel0=0 "Unstretched spring length";
7: 
```

[Mechanics/Translational/Components/Spring.mo — source snapshot](../evidence/sources/761ca23f5d4162a3-Spring.mo)

```modelica
2: model Spring "Linear 1D translational spring"
3:   extends Translational.Interfaces.PartialCompliant;
4:   parameter SI.TranslationalSpringConstant c(final min=0, start=1)
5:     "Spring constant";
6:   parameter SI.Distance s_rel0=0 "Unstretched spring length";
7: 
8: equation
9:   f = c*(s_rel - s_rel0);
10:   annotation (
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/0b94fd5a2113d8fb.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-spring-stiffness.md) · [Index](../README.md)
