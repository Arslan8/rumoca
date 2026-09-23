# FINDING-02701: Air-gap inductance is used as a flux multiplier

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-machine-airgap-inductance |
| Model | Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer |
| Target | aimc.airGap.Lm |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-transformer-aimc-airgap-lm-zerolimit-2.md](../../v2/bugs/FINDING-imc-transformer-aimc-airgap-lm-zerolimit-2.md) — reviewed as `FINDING-02701-imc-transformer-aimc-airgap-lm.md`, which a later run renamed |
| Original SHA-256 | 4e9da43f2bad94435ebcafefe42c8358ad86874d707d61b4cbffb97fcb131b4e |

## Why this is a false positive

The air-gap model constructs an inductance matrix and computes psi=L*i. Neither the main inductance nor the protected matrix is divided. Zero removes the corresponding magnetic coupling; a useful machine normally needs coupling, but that engineering expectation is not an intrinsic arithmetic-domain failure.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/Components/AirGapS.mo:3`. Role: `parameter`; binding: `aimcData.Lm`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/Components/AirGapS.mo — source snapshot](../evidence/sources/564deb47f89b9ee1-AirGapS.mo)

```modelica
1: within Modelica.Electrical.Machines.BasicMachines.Components;
2: model AirGapS "Airgap in stator-fixed coordinate system"
3:   parameter SI.Inductance Lm "Main field inductance";
4:   extends PartialAirGap;
5:   SI.Current i_ms[2]
6:     "Magnetizing current space phasor with respect to the stator fixed frame";
```

[Electrical/Machines/BasicMachines/Components/AirGapS.mo — source snapshot](../evidence/sources/564deb47f89b9ee1-AirGapS.mo)

```modelica
2: model AirGapS "Airgap in stator-fixed coordinate system"
3:   parameter SI.Inductance Lm "Main field inductance";
4:   extends PartialAirGap;
5:   SI.Current i_ms[2]
6:     "Magnetizing current space phasor with respect to the stator fixed frame";
7: protected
8:   parameter SI.Inductance L[2, 2]={{Lm,0},{0,Lm}}
9:     "Inductance matrix";
10: equation
11:   // Magnetizing current with respect to the stator reference frame
12:   i_ms = i_ss + i_rs;
13:   // Magnetizing flux linkage with respect to the stator reference frame
14:   psi_ms = L*i_ms;
15:   // Magnetizing flux linkage with respect to the rotor reference frame
16:   psi_mr = transpose(RotationMatrix)*psi_ms;
17:   annotation (
18:     defaultComponentName="airGap",
19:     Icon(coordinateSystem(preserveAspectRatio=true, extent={{-100,-100},{
20:             100,100}}), graphics={Text(
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/1d64c76f1b77946f.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-machine-airgap-inductance.md) · [Index](../README.md)
