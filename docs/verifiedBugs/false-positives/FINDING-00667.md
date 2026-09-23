# FINDING-00667: The complete conductor denominator is already asserted positive

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | guarded-temperature-factor |
| Model | Modelica.Electrical.Analog.Examples.Lines.SmoothStep |
| Target | oLine50.G[12].T_ref |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-00667-smoothstep-oline50-g-12-t-ref.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 952ab3593d39d72e6fc1eb5d0ba616a2040c9aa6252e2efa257bbb6665d11d93 |

## Why this is a false positive

The denominator is 1+alpha*(T_heatPort-T_ref), not alpha or T_ref alone. An existing assertion requires that complete expression >= Modelica.Constants.eps. In particular alpha=0 makes the denominator 1, not zero. The report ignores the constant term and existing whole-expression domain check. An invalid-temperature assertion is intended rejection, not a newly verified divide-by-zero bug.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Basic/Conductor.mo:5`. Role: `parameter`; binding: `300.15`; effective min: `0.0`; effective max: `None`. 

[Electrical/Analog/Basic/Conductor.mo — source snapshot](../evidence/sources/ba7d0584ed688761-Conductor.mo)

```modelica
3:   parameter SI.Conductance G(start=1)
4:     "Conductance at temperature T_ref";
5:   parameter SI.Temperature T_ref=300.15 "Reference temperature";
6:   parameter SI.LinearTemperatureCoefficient alpha=0
7:     "Temperature coefficient of conductance (G_actual = G_ref/(1 + alpha*(T_heatPort - T_ref))";
8:   extends Modelica.Electrical.Analog.Interfaces.OnePort;
```

[Electrical/Analog/Basic/Conductor.mo — source snapshot](../evidence/sources/ba7d0584ed688761-Conductor.mo)

```modelica
5:   parameter SI.Temperature T_ref=300.15 "Reference temperature";
6:   parameter SI.LinearTemperatureCoefficient alpha=0
7:     "Temperature coefficient of conductance (G_actual = G_ref/(1 + alpha*(T_heatPort - T_ref))";
8:   extends Modelica.Electrical.Analog.Interfaces.OnePort;
9:   extends Modelica.Electrical.Analog.Interfaces.ConditionalHeatPort(T=T_ref);
10:   SI.Conductance G_actual
11:     "Actual conductance = G_ref/(1 + alpha*(T_heatPort - T_ref))";
12: 
13: equation
14:   assert((1 + alpha*(T_heatPort - T_ref)) >= Modelica.Constants.eps,
15:     "Temperature outside scope of model!");
16:   G_actual = G/(1 + alpha*(T_heatPort - T_ref));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/21f9fcbcb956ec17.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/guarded-temperature-factor.md) · [Index](../README.md)
