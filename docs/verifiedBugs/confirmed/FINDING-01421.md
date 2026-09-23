# FINDING-01421: Zero nominal excitation flux divides the turns-ratio calculation

| Field | Value |
|---|---|
| Verdict | confirmed |
| Scope / group | dc-machine-flux-scale |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Temperature |
| Target | dcpm.psi_eNominal |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-01421-dcpm-temperature-dcpm-psi-enominal.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 2f383cc05e296a6c91000a2c11ff86012d17748d06b39e01b4f1ea542f564fac |

## Verification and root cause

PartialBasicDCMachine declares psi_eNominal without a positive/nonzero constraint and computes turnsRatio=ViNominal/(wNominal*psi_eNominal). Zero excitation flux therefore makes the machine scaling undefined. This is a direct source denominator even when a full example is blocked by unrelated runtime support.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Interfaces/PartialBasicDCMachine.mo:98`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Interfaces/PartialBasicDCMachine.mo — source snapshot](../evidence/sources/4db8b5f43a5834a2-PartialBasicDCMachine.mo)

```modelica
96:     annotation (Evaluate=true);
97:   parameter SI.Voltage ViNominal "Nominal induced Voltage";
98:   parameter SI.MagneticFlux psi_eNominal
99:     "Nominal magnetic flux";
100:   parameter Real turnsRatio=ViNominal/(wNominal*psi_eNominal)
101:     "Ratio of armature turns over number of turns of the excitation winding";
```

[Electrical/Machines/Interfaces/PartialBasicDCMachine.mo — source snapshot](../evidence/sources/4db8b5f43a5834a2-PartialBasicDCMachine.mo)

```modelica
94:   constant Real pi = Modelica.Constants.pi;
95:   constant Boolean quasiStatic=false "No electrical transients if true"
96:     annotation (Evaluate=true);
97:   parameter SI.Voltage ViNominal "Nominal induced Voltage";
98:   parameter SI.MagneticFlux psi_eNominal
99:     "Nominal magnetic flux";
100:   parameter Real turnsRatio=ViNominal/(wNominal*psi_eNominal)
101:     "Ratio of armature turns over number of turns of the excitation winding";
102:   replaceable Machines.Interfaces.DCMachines.PartialThermalPortDCMachines internalThermalPort
103:     annotation (Placement(transformation(extent={{-4,-84},{4,-76}})));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f6a744925526df08.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Proposed fix

Define the intended sign convention, then require abs(psi_eNominal)>=small (or psi_eNominal>0) and validate it before computing turnsRatio. A zero-flux motor requires a separate degenerate formulation, not epsilon substitution.

## Fix validation

Test the nominal machine, valid polarity if supported, zero and near-zero flux, and zero nominal speed independently so diagnostics identify the correct invalid scale.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/dc-machine-flux-scale.md) · [Index](../README.md)
