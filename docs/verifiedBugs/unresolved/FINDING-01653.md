# FINDING-01653: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive |
| Target | RGrid |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-inverterdrive-rgrid-ruleoff.md](../../v2/bugs/FINDING-imc-inverterdrive-rgrid-ruleoff.md) — reviewed as `FINDING-01653-imc-inverterdrive-rgrid.md`, which a later run renamed |
| Original SHA-256 | c61135d378f885810fd33418b1bb980b56570f4d318ea2902c9b469fe9fa271b |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/InductionMachines/IMC_InverterDrive.mo:11`. Role: `parameter`; binding: `0.01`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/InductionMachines/IMC_InverterDrive.mo — source snapshot](../evidence/sources/35d82484be6d95ca-IMC_InverterDrive.mo)

```modelica
9:     "Nominal RMS voltage per phase";
10:   parameter SI.Frequency fNominal=50 "Nominal frequency";
11:   parameter SI.Resistance RGrid=10e-3 "Grid choke resistance";
12:   parameter SI.Inductance LGrid=500e-6 "Grid choke inductance";
13:   parameter SI.Voltage VDC=factorY2DC(m)*VNominal/sqrt(3) "Theoretical DC voltage";
14:   parameter SI.Capacitance CDC=5e-3 "DC capacitor";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f1b3b20d1746a2aa.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
