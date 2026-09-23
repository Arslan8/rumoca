# FINDING-03653: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.DCDC.HBridge.HBridge_R |
| Target | hbridge.GoffDiode |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-hbridge-r-hbridge-goffdiode-intent.md](../../v2/bugs/FINDING-hbridge-r-hbridge-goffdiode-intent.md) — reviewed as `FINDING-03653-hbridge-r-hbridge-goffdiode.md`, which a later run renamed |
| Original SHA-256 | 5051f4838f47f1b89fb8ce3482e7bbcc2bfbbbeb27167652763b6c9ce3fc718a |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/DCDC/HBridge.mo:16`. Role: `parameter`; binding: `1e-05`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/DCDC/HBridge.mo — source snapshot](../evidence/sources/c29a16811f4c814b-HBridge.mo)

```modelica
14:   parameter SI.Resistance RonDiode=1e-05
15:     "Diode closed resistance";
16:   parameter SI.Conductance GoffDiode=1e-05
17:     "Diode opened conductance";
18:   parameter SI.Voltage VkneeDiode=0 "Diode threshold voltage";
19:   extends Interfaces.Enable.Enable2;
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/9ec1246440080430.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
