# FINDING-04687: Zero thermal conductance is an insulating limit

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-thermal-conductance |
| Model | Modelica.Thermal.FluidHeatFlow.Examples.TwoMass |
| Target | thermalConductor1.G |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-twomass-thermalconductor1-g-zerolimit.md](../../v2/bugs/FINDING-twomass-thermalconductor1-g-zerolimit.md) — reviewed as `FINDING-04687-twomass-thermalconductor1-g.md`, which a later run renamed |
| Original SHA-256 | d0ca4ff6d19e27a64b067f6c8d444b7d1de935a8cfedc3d3286f2766d139b7c7 |

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

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/fde7c27d63ef89cc.json). Baseline: **clean**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-thermal-conductance.md) · [Index](../README.md)
