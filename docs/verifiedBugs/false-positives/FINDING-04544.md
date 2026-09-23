# FINDING-04544: Zero thermal conductance is an insulating limit

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-thermal-conductance |
| Model | Modelica.Thermal.FluidHeatFlow.Examples.OneMass |
| Target | thermalConductor.G |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-onemass-thermalconductor-g-zerolimit.md](../../v2/bugs/FINDING-onemass-thermalconductor-g-zerolimit.md) — reviewed as `FINDING-04544-onemass-thermalconductor-g.md`, which a later run renamed |
| Original SHA-256 | 8bf278141a6190ffc3277ed5c8ef8e624d9f9056837172ae17a002e0545504a6 |

## Why this is a false positive

The complete constitutive equation is Q_flow=G*dT. G is only a multiplier; at zero the component transports no heat. There is no source reciprocal and the component represents a lumped effective conductance, so a blanket strictly-positive claim rejects the ordinary insulation/open-thermal-path limit. A larger network may still need another equation for each isolated temperature.

## Source evidence

Compiler/source-resolved declaration: `Thermal/HeatTransfer/Components/ThermalConductor.mo:5`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Thermal/HeatTransfer/Components/ThermalConductor.mo — source snapshot](../evidence/sources/048e3d7f05b4a2df-ThermalConductor.mo)

```modelica
3:   "Lumped thermal element transporting heat without storing it"
4:   extends Interfaces.Element1D;
5:   parameter SI.ThermalConductance G
6:     "Constant thermal conductance of material";
7: 
8: equation
```

[Thermal/HeatTransfer/Components/ThermalConductor.mo — source snapshot](../evidence/sources/048e3d7f05b4a2df-ThermalConductor.mo)

```modelica
2: model ThermalConductor
3:   "Lumped thermal element transporting heat without storing it"
4:   extends Interfaces.Element1D;
5:   parameter SI.ThermalConductance G
6:     "Constant thermal conductance of material";
7: 
8: equation
9:   Q_flow = G*dT;
10:   annotation (
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/70576a1588e71f74.json). Baseline: **clean**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-thermal-conductance.md) · [Index](../README.md)
