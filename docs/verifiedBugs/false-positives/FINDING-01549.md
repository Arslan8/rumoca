# FINDING-01549: Zero space-phasor inductance is an algebraic ideal limit

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-space-phasor-inductance |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DCBraking |
| Target | imc.lssigma.L |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-dcbraking-imc-lssigma-l-intent.md](../../v2/bugs/FINDING-imc-dcbraking-imc-lssigma-l-intent.md) — reviewed as `FINDING-01549-imc-dcbraking-imc-lssigma-l.md`, which a later run renamed |
| Original SHA-256 | eafa09e688b70c3c2638e409516cdb545be9abf580ffe4d6d22e58e2c0499483 |

## Why this is a false positive

Both axis equations are v_[j]=L[j]*der(i_[j]); L is a multiplier and is never divided. A zero entry sets the corresponding voltage drop to zero. The report applies a strictly-positive heuristic where the component equations support an ideal zero-leakage limit.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/Components/Inductor.mo:3`. Role: `parameter`; binding: `fill(imc.Lssigma, 2)`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/Components/Inductor.mo — source snapshot](../evidence/sources/aa9e7749276e6b4a-Inductor.mo)

```modelica
1: within Modelica.Electrical.Machines.BasicMachines.Components;
2: model Inductor "Space phasor inductor"
3:   parameter SI.Inductance L[2] "Inductance of both axes";
4:   SI.Voltage v_[2];
5:   SI.Current i_[2];
6:   Machines.Interfaces.SpacePhasor spacePhasor_a
```

[Electrical/Machines/BasicMachines/Components/Inductor.mo — source snapshot](../evidence/sources/aa9e7749276e6b4a-Inductor.mo)

```modelica
2: model Inductor "Space phasor inductor"
3:   parameter SI.Inductance L[2] "Inductance of both axes";
4:   SI.Voltage v_[2];
5:   SI.Current i_[2];
6:   Machines.Interfaces.SpacePhasor spacePhasor_a
7:     annotation (Placement(transformation(extent={{-110,-10},{-90,10}})));
8:   Machines.Interfaces.SpacePhasor spacePhasor_b
9:     annotation (Placement(transformation(extent={{90,-10},{110,10}})));
10: equation
11:   spacePhasor_a.i_ + spacePhasor_b.i_ = zeros(2);
12:   v_ = spacePhasor_a.v_ - spacePhasor_b.v_;
13:   i_ = spacePhasor_a.i_;
14:   v_[1] = L[1]*der(i_[1]);
15:   v_[2] = L[2]*der(i_[2]);
16:   annotation (Documentation(info="<html>
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/489fdf592354cb9a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-space-phasor-inductance.md) · [Index](../README.md)
