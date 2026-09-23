# FINDING-00164: Signed resistance is intentional and the divisor is bounded away from zero

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | switched-capacitor-guard |
| Model | Modelica.Electrical.Analog.Examples.CauerLowPassSC |
| Target | R2.oneOhm |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-cauerlowpasssc-r2-oneohm-zerolimit.md](../../v2/bugs/FINDING-cauerlowpasssc-r2-oneohm-zerolimit.md) — reviewed as `FINDING-00164-cauerlowpasssc-r2-oneohm.md`, which a later run renamed |
| Original SHA-256 | a7889ed947ddf5a93938f461f2119f5f3382e356e5796103a5347342f5e081cf |

## Why this is a false positive

The model explicitly represents positive or negative resistance. Its capacitance uses clock/max(eps*oneOhm,abs(R)), where protected constant oneOhm=1. Thus R=0 does not zero the denominator, negative R is handled by abs, and oneOhm is a fixed unit-conversion constant in this model rather than a reported adjustable parameter.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/Utilities/SwitchedCapacitor.mo:30`. Role: `constant`; binding: `1`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/Utilities/SwitchedCapacitor.mo — source snapshot](../evidence/sources/a4b15fe7b64a11d8-SwitchedCapacitor.mo)

```modelica
28:   Modelica.Blocks.Logical.LogicalSwitch logicalSwitch annotation (Placement(transformation(extent={{-20,20},{-40,40}})));
29: protected
30:   constant SI.Resistance oneOhm=1 "Helping constant to satisfy unit check";
31: equation
32:   connect(IdealCommutingSwitch1.p, Capacitor.p) annotation (Line(points={{-40,0},{-40,0},{-44,0},{-20,0}}, color={0,0,255}));
33:   connect(Capacitor.n, IdealCommutingSwitch2.p) annotation (Line(points={{20,0},{25,0},{30,0},{40,0}}, color={0,0,255}));
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
