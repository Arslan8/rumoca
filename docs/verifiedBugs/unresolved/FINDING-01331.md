# FINDING-01331: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Drive |
| Target | dcdcInverter2.RonD |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-dcpm-drive-dcdcinverter2-rond-intent.md](../../v2/bugs/FINDING-dcpm-drive-dcdcinverter2-rond-intent.md) — reviewed as `FINDING-01331-dcpm-drive-dcdcinverter2-rond.md`, which a later run renamed |
| Original SHA-256 | b79002fd43cfe26fd6a50cb487d2f6fafed2b2f30c36e48a46d9efc7149055b6 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/ControlledDCDrives/Utilities/DcdcInverter.mo:19`. Role: `parameter`; binding: `1e-05`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/ControlledDCDrives/Utilities/DcdcInverter.mo — source snapshot](../evidence/sources/540ec26d119f3ecf-DcdcInverter.mo)

```modelica
17:     "Transistor threshold voltage"
18:     annotation (Dialog(group="Switching", enable=not useIdealInverter));
19:   parameter SI.Resistance RonD=1e-05
20:     "Diode closed resistance"
21:     annotation (Dialog(group="Switching", enable=not useIdealInverter));
22:   parameter SI.Conductance GoffD=1e-05
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/3f243142a2b979d6.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
