# FINDING-01488: AirGapDC uses excitation inductance only as a multiplier

| Field | Value |
|---|---|
| Verdict | false-positives |
| Scope / group | zero-dc-airgap-inductance |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCSE_SinglePhase |
| Target | dcse.airGapDC.Le |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-dcse-singlephase-dcse-airgapdc-le-zerolimit.md](../../v2/bugs/FINDING-dcse-singlephase-dcse-airgapdc-le-zerolimit.md) — reviewed as `FINDING-01488-dcse-singlephase-dcse-airgapdc-le.md`, which a later run renamed |
| Original SHA-256 | 8f7470d5aea7b2847ceb69769da22b123e301ccd52c58490afad874ac3602783 |

## Why this is a false positive

The complete magnetic relation is psi_e=Le*ie. Le=0 produces zero excitation flux; this source does not divide by Le. Whether such an idealized machine remains useful is separate from the reported claim that the declaration necessarily causes an arithmetic failure.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/Components/AirGapDC.mo:4`. Role: `parameter`; binding: `dcse.Lme`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/Components/AirGapDC.mo — source snapshot](../evidence/sources/c1c977b6397a4f82-AirGapDC.mo)

```modelica
2: model AirGapDC "Linear airgap model of a DC machine"
3:   extends PartialAirGapDC;
4:   parameter SI.Inductance Le "Excitation inductance";
5: equation
6:   // excitation flux: linearly dependent on excitation current
7:   psi_e = Le*ie;
```

[Electrical/Machines/BasicMachines/Components/AirGapDC.mo — source snapshot](../evidence/sources/c1c977b6397a4f82-AirGapDC.mo)

```modelica
2: model AirGapDC "Linear airgap model of a DC machine"
3:   extends PartialAirGapDC;
4:   parameter SI.Inductance Le "Excitation inductance";
5: equation
6:   // excitation flux: linearly dependent on excitation current
7:   psi_e = Le*ie;
8:   annotation (
9:     defaultComponentName="airGap",
10:     Documentation(info="<html>
11: Linear model of the airgap (without saturation effects) of a DC machine, using only equations.<br>
12: Induced excitation voltage is calculated from der(flux), where flux is defined by excitation inductance times excitation current.<br>
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f00103fd4bc29b1a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Correct the detector/adjudicator for this specific semantic case; do not impose a blanket strictly-positive bound on the library declaration.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/zero-dc-airgap-inductance.md) · [Index](../README.md)
