# FINDING-04464: Zero stiffness is a force-free spring limit

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-spring-stiffness |
| Model | Modelica.Mechanics.Translational.Examples.Oscillator |
| Target | spring1.c |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-oscillator-spring1-c-zerolimit.md](../../v2/bugs/FINDING-oscillator-spring1-c-zerolimit.md) — reviewed as `FINDING-04464-oscillator-spring1-c.md`, which a later run renamed |
| Original SHA-256 | 6543a0196cc9ae59f7a7d3694d9d0c506d9dde3c3ea8faa52e60cdc25e569163 |

## Why this is a false positive

The constitutive equation multiplies displacement by c (f=c*(s_rel-s_rel0) or tau=c*(phi_rel-phi_rel0)). At c=0 it transmits no elastic force; there is no reciprocal and the declaration intentionally has min=0. A disconnected or under-constrained surrounding mechanism is topology-specific, not proof that the component bound is defective.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Translational/Components/Spring.mo:4`. Role: `parameter`; binding: `10000`; effective min: `0`; effective max: `None`. 

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

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/9274b293950a5bd6.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-spring-stiffness.md) · [Index](../README.md)
