# FINDING-02429: Air-gap inductance is used as a flux multiplier

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-machine-airgap-inductance |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMPM_NoLoad |
| Target | smpm.airGap.Lmd |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smpm-noload-smpm-airgap-lmd-zerolimit.md](../../v2/bugs/FINDING-smpm-noload-smpm-airgap-lmd-zerolimit.md) — reviewed as `FINDING-02429-smpm-noload-smpm-airgap-lmd.md`, which a later run renamed |
| Original SHA-256 | 99aed4666892bb31e6faa77d44d03f721384fccf0d23ce6d18c28db25eee9c99 |

## Why this is a false positive

The air-gap model constructs an inductance matrix and computes psi=L*i. Neither the main inductance nor the protected matrix is divided. Zero removes the corresponding magnetic coupling; a useful machine normally needs coupling, but that engineering expectation is not an intrinsic arithmetic-domain failure.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/Components/AirGapR.mo:3`. Role: `parameter`; binding: `smpmData.Lmd`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/Components/AirGapR.mo — source snapshot](../evidence/sources/239b41ad1647cfdf-AirGapR.mo)

```modelica
1: within Modelica.Electrical.Machines.BasicMachines.Components;
2: model AirGapR "Airgap in rotor-fixed coordinate system"
3:   parameter SI.Inductance Lmd
4:     "Main field inductance d-axis";
5:   parameter SI.Inductance Lmq
6:     "Main field inductance q-axis";
```

[Electrical/Machines/BasicMachines/Components/AirGapR.mo — source snapshot](../evidence/sources/239b41ad1647cfdf-AirGapR.mo)

```modelica
2: model AirGapR "Airgap in rotor-fixed coordinate system"
3:   parameter SI.Inductance Lmd
4:     "Main field inductance d-axis";
5:   parameter SI.Inductance Lmq
6:     "Main field inductance q-axis";
7:   extends PartialAirGap;
8:   SI.Current i_mr[2]
9:     "Magnetizing current space phasor with respect to the rotor fixed frame";
10: protected
11:   parameter SI.Inductance L[2, 2]={{Lmd,0},{0,Lmq}}
12:     "Inductance matrix";
13: equation
14:   // Magnetizing current with respect to the rotor reference frame
15:   i_mr = i_sr + i_rr;
16:   // Main flux linkage with respect to the rotor reference frame
17:   psi_mr = L*i_mr;
18:   // Main flux linkage with respect to the stator reference frame
19:   psi_ms = RotationMatrix*psi_mr;
20:   annotation (
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/dd1bf4e5a4d0a401.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-machine-airgap-inductance.md) · [Index](../README.md)
