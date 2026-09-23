# FINDING-05026: Zero stiffness/damping disables one parallel force term

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-spring-damper-term |
| Model | ModelicaTest.Translational.AllComponents |
| Target | springDamper.c |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-allcomponents-springdamper-c-zerolimit.md](../../v2/bugs/FINDING-allcomponents-springdamper-c-zerolimit.md) — reviewed as `FINDING-05026-allcomponents-springdamper-c.md`, which a later run renamed |
| Original SHA-256 | 8f7cb7937992af1eea6d9affeb144e2a4b46547f01251e7f3bcfe346eb40fde4 |

## Why this is a false positive

The equations are f_c=c*(s_rel-s_rel0), f_d=d*v_rel and f=f_c+f_d. Both parameters are multipliers with min=0; zero cleanly removes the corresponding elastic or dissipative term. It is not an intrinsic division or invalid bound.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Translational/Components/SpringDamper.mo:4`. Role: `parameter`; binding: `1`; effective min: `0`; effective max: `None`. 

[Mechanics/Translational/Components/SpringDamper.mo — source snapshot](../evidence/sources/5673e9802b6f2bf4-SpringDamper.mo)

```modelica
2: model SpringDamper "Linear 1D translational spring and damper in parallel"
3:   extends Translational.Interfaces.PartialCompliantWithRelativeStates;
4:   parameter SI.TranslationalSpringConstant c(final min=0, start=1)
5:     "Spring constant";
6:   parameter SI.TranslationalDampingConstant d(final min=0, start=1)
7:     "Damping constant";
```

[Mechanics/Translational/Components/SpringDamper.mo — source snapshot](../evidence/sources/5673e9802b6f2bf4-SpringDamper.mo)

```modelica
2: model SpringDamper "Linear 1D translational spring and damper in parallel"
3:   extends Translational.Interfaces.PartialCompliantWithRelativeStates;
4:   parameter SI.TranslationalSpringConstant c(final min=0, start=1)
5:     "Spring constant";
6:   parameter SI.TranslationalDampingConstant d(final min=0, start=1)
7:     "Damping constant";
8:   parameter SI.Position s_rel0=0 "Unstretched spring length";
9:   extends Modelica.Thermal.HeatTransfer.Interfaces.PartialElementaryConditionalHeatPortWithoutT;
10: protected
11:   SI.Force f_c "Spring force";
12:   SI.Force f_d "Damping force";
13: equation
14:   f_c = c*(s_rel - s_rel0);
15:   f_d = d*v_rel;
16:   f = f_c + f_d;
17:   lossPower = f_d*v_rel;
18:   annotation (
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/a006880b61697aee.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-spring-damper-term.md) · [Index](../README.md)
