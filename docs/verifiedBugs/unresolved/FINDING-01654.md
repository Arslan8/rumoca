# FINDING-01654: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive |
| Target | LGrid |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-inverterdrive-lgrid-zerolimit.md](../../v2/bugs/FINDING-imc-inverterdrive-lgrid-zerolimit.md) — reviewed as `FINDING-01654-imc-inverterdrive-lgrid.md`, which a later run renamed |
| Original SHA-256 | da9b442fb1b2dfd197ab756aaa15b70c279347850e9fdd199f6d381e14c52265 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/InductionMachines/IMC_InverterDrive.mo:12`. Role: `parameter`; binding: `0.0005`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/InductionMachines/IMC_InverterDrive.mo — source snapshot](../evidence/sources/35d82484be6d95ca-IMC_InverterDrive.mo)

```modelica
10:   parameter SI.Frequency fNominal=50 "Nominal frequency";
11:   parameter SI.Resistance RGrid=10e-3 "Grid choke resistance";
12:   parameter SI.Inductance LGrid=500e-6 "Grid choke inductance";
13:   parameter SI.Voltage VDC=factorY2DC(m)*VNominal/sqrt(3) "Theoretical DC voltage";
14:   parameter SI.Capacitance CDC=5e-3 "DC capacitor";
15:   parameter SI.Torque TLoad=161.4 "Nominal load torque";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f1b3b20d1746a2aa.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
