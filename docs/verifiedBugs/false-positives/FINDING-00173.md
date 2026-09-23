# FINDING-00173: Signed resistance is intentional and the divisor is bounded away from zero

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | switched-capacitor-guard |
| Model | Modelica.Electrical.Analog.Examples.CauerLowPassSC |
| Target | R10.R |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-cauerlowpasssc-r10-r-ruleoff.md](../../v2/bugs/FINDING-cauerlowpasssc-r10-r-ruleoff.md) — reviewed as `FINDING-00173-cauerlowpasssc-r10-r.md`, which a later run renamed |
| Original SHA-256 | 0d2315b5a5cf4a7121e30017314f5bcdd8d5ca1375788243f351f8ed35ab87e0 |

## Why this is a false positive

The model explicitly represents positive or negative resistance. Its capacitance uses clock/max(eps*oneOhm,abs(R)), where protected constant oneOhm=1. Thus R=0 does not zero the denominator, negative R is handled by abs, and oneOhm is a fixed unit-conversion constant in this model rather than a reported adjustable parameter.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/Utilities/SwitchedCapacitor.mo:5`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/Utilities/SwitchedCapacitor.mo — source snapshot](../evidence/sources/a4b15fe7b64a11d8-SwitchedCapacitor.mo)

```modelica
3: 
4:   parameter SI.Time clock(start=1) "Clock";
5:   parameter SI.Resistance R(start=1) "Resistance";
6:   Modelica.Blocks.Sources.BooleanPulse BooleanPulse(period=clock) annotation (Placement(transformation(extent={{-8,70},{12,90}})));
7:   Modelica.Electrical.Analog.Basic.Capacitor Capacitor(C=clock/max(Modelica.Constants.eps*oneOhm,abs(R)))
8:                                                                   annotation (Placement(transformation(extent={{-20,-20},{20,20}})));
```

[Electrical/Analog/Examples/Utilities/SwitchedCapacitor.mo — source snapshot](../evidence/sources/a4b15fe7b64a11d8-SwitchedCapacitor.mo)

```modelica
1: within Modelica.Electrical.Analog.Examples.Utilities;
2: model SwitchedCapacitor "Switched capacitor which can represent a positive or negative resistance"
3: 
4:   parameter SI.Time clock(start=1) "Clock";
5:   parameter SI.Resistance R(start=1) "Resistance";
6:   Modelica.Blocks.Sources.BooleanPulse BooleanPulse(period=clock) annotation (Placement(transformation(extent={{-8,70},{12,90}})));
7:   Modelica.Electrical.Analog.Basic.Capacitor Capacitor(C=clock/max(Modelica.Constants.eps*oneOhm,abs(R)))
```

[Electrical/Analog/Examples/Utilities/SwitchedCapacitor.mo — source snapshot](../evidence/sources/a4b15fe7b64a11d8-SwitchedCapacitor.mo)

```modelica
29: protected
30:   constant SI.Resistance oneOhm=1 "Helping constant to satisfy unit check";
```

[Electrical/Analog/Examples/Utilities/SwitchedCapacitor.mo — source snapshot](../evidence/sources/a4b15fe7b64a11d8-SwitchedCapacitor.mo)

```modelica
70:       Documentation(info="<html>
71: <p>This model is a switched capacitor model without thermal behavior which can represent positive and negative resistances.</p>
72: <p>The clock source is inside the model, its frequency can be chosen by a parameter.
73: Also the resistance is a parameter which can be positive and negative.
74: The internal (switched) capacitor is parametrized in such a way that the total resistance is independently from the frequency equal to the resistance parameter.</p>
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f208d9a532ab730d.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/switched-capacitor-guard.md) · [Index](../README.md)
