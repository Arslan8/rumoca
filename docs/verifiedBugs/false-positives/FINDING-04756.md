# FINDING-04756: Zero heat capacity is a no-storage algebraic limit

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-heat-capacity |
| Model | Modelica.Thermal.HeatTransfer.Examples.GenerationOfFMUs |
| Target | directCapacity.heatCapacitor.C |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-generationoffmus-directcapacity-heatcapacitor-c-zerolimit.md](../../v2/bugs/FINDING-generationoffmus-directcapacity-heatcapacitor-c-zerolimit.md) — reviewed as `FINDING-04756-generationoffmus-directcapacity-heatcapacitor-c.md`, which a later run renamed |
| Original SHA-256 | 95e1c45910907f175bba65904f682e9d2d8a77809214b7c41584fdf0397525bf |

## Why this is a false positive

The source equation is C*der(T)=port.Q_flow, not division by C. At C=0 it imposes zero stored heat flow and removes the temperature state. Thus the missing/zero-bound claim does not by itself prove a defect; fixed starts or isolated thermal topologies may still become inconsistent. The two divisor-reach reports for this declaration remain unresolved separately because they make a different compiler-IR claim.

## Source evidence

Compiler/source-resolved declaration: `Thermal/HeatTransfer/Components/HeatCapacitor.mo:3`. Role: `parameter`; binding: `1.1`; effective min: `None`; effective max: `None`. 

[Thermal/HeatTransfer/Components/HeatCapacitor.mo — source snapshot](../evidence/sources/98ab41cf170afbb5-HeatCapacitor.mo)

```modelica
1: within Modelica.Thermal.HeatTransfer.Components;
2: model HeatCapacitor "Lumped thermal element storing heat"
3:   parameter SI.HeatCapacity C
4:     "Heat capacity of element (= cp*m)";
5:   SI.Temperature T(start=293.15, displayUnit="degC")
6:     "Temperature of element";
```

[Thermal/HeatTransfer/Components/HeatCapacitor.mo — source snapshot](../evidence/sources/98ab41cf170afbb5-HeatCapacitor.mo)

```modelica
2: model HeatCapacitor "Lumped thermal element storing heat"
3:   parameter SI.HeatCapacity C
4:     "Heat capacity of element (= cp*m)";
5:   SI.Temperature T(start=293.15, displayUnit="degC")
6:     "Temperature of element";
7:   SI.TemperatureSlope der_T(start=0)
8:     "Time derivative of temperature (= der(T))";
9:   Interfaces.HeatPort_a port annotation (Placement(transformation(
10:         origin={0,-100},
11:         extent={{-10,-10},{10,10}},
12:         rotation=90)));
13: equation
14:   T = port.T;
15:   der_T = der(T);
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/ee1001c8dcf1bc50.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-heat-capacity.md) · [Index](../README.md)
