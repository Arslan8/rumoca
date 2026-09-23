# FINDING-01344: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive |
| Target | dcdcInverter1.Ti |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-01344-dcpm-drive-dcdcinverter1-ti.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 1b8e3a09b8307a8d3bc06b8d8259c07b51586d3f163808cc1433718dba2e27d2 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/ControlledDCDrives/Utilities/DcdcInverter.mo:8`. Role: `parameter`; binding: `1e-06`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/ControlledDCDrives/Utilities/DcdcInverter.mo — source snapshot](../evidence/sources/540ec26d119f3ecf-DcdcInverter.mo)

```modelica
6:   parameter SI.Time Tmf=2/fS "Measurement filter time constant";
7:   parameter SI.Voltage VMax "Maximum Voltage";
8:   parameter SI.Time Ti=1e-6 "Time constant of integral power controller"
9:     annotation(Dialog(group="Averaging", enable=useIdealInverter));
10:   parameter SI.Resistance RonT=1e-05
11:     "Transistor closed resistance"
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/3f243142a2b979d6.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
