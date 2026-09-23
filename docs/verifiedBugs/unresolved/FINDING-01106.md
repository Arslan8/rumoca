# FINDING-01106: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.ControlledDCDrives.Utilities.DcdcInverter |
| Target | RonT |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-dcdcinverter-ront-intent.md](../../v2/bugs/FINDING-dcdcinverter-ront-intent.md) — reviewed as `FINDING-01106-dcdcinverter-ront.md`, which a later run renamed |
| Original SHA-256 | 0e9f131750583113b4c43e5ea141ecbd860c36b7bdaeed65acf4482462cc3934 |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/ControlledDCDrives/Utilities/DcdcInverter.mo:10`. Role: `parameter`; binding: `1e-05`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/ControlledDCDrives/Utilities/DcdcInverter.mo — source snapshot](../evidence/sources/540ec26d119f3ecf-DcdcInverter.mo)

```modelica
8:   parameter SI.Time Ti=1e-6 "Time constant of integral power controller"
9:     annotation(Dialog(group="Averaging", enable=useIdealInverter));
10:   parameter SI.Resistance RonT=1e-05
11:     "Transistor closed resistance"
12:     annotation (Dialog(group="Switching", enable=not useIdealInverter));
13:   parameter SI.Conductance GoffT=1e-05
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/5c10b98e9c2107be.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
