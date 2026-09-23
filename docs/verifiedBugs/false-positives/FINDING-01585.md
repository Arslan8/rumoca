# FINDING-01585: Air-gap inductance is used as a flux multiplier

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-machine-airgap-inductance |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_DOL |
| Target | aimc.airGap.L |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-dol-aimc-airgap-l-zerolimit.md](../../v2/bugs/FINDING-imc-dol-aimc-airgap-l-zerolimit.md) — reviewed as `FINDING-01585-imc-dol-aimc-airgap-l.md`, which a later run renamed |
| Original SHA-256 | 5a160f2876fecd139639828af9c30ecf6cf694a22487c3de3c9408c33b4c333e |

## Why this is a false positive

The air-gap model constructs an inductance matrix and computes psi=L*i. Neither the main inductance nor the protected matrix is divided. Zero removes the corresponding magnetic coupling; a useful machine normally needs coupling, but that engineering expectation is not an intrinsic arithmetic-domain failure.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/Components/AirGapS.mo:8`. Role: `parameter`; binding: `{{aimc.airGap.Lm, 0}, {0, aimc.airGap.Lm}}`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/Components/AirGapS.mo — source snapshot](../evidence/sources/564deb47f89b9ee1-AirGapS.mo)

```modelica
6:     "Magnetizing current space phasor with respect to the stator fixed frame";
7: protected
8:   parameter SI.Inductance L[2, 2]={{Lm,0},{0,Lm}}
9:     "Inductance matrix";
10: equation
11:   // Magnetizing current with respect to the stator reference frame
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

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/3bb307101f6982f2.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-machine-airgap-inductance.md) · [Index](../README.md)
