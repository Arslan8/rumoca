# FINDING-00806: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.DifferentialAmplifier |
| Target | data.RLoad |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-differentialamplifier-data-rload-zerolimit.md](../../v2/bugs/FINDING-differentialamplifier-data-rload-zerolimit.md) — reviewed as `FINDING-00806-differentialamplifier-data-rload.md`, which a later run renamed |
| Original SHA-256 | dd3d2bec939a9ff465b0698b6b9cf12a41e00fec278ba680d939b0025b1347b8 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/DifferentialAmplifierData.mo:8`. Role: `parameter`; binding: `10`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/OpAmpCircuits/DifferentialAmplifierData.mo — source snapshot](../evidence/sources/0cea00d163c1f4d9-DifferentialAmplifierData.mo)

```modelica
6:   parameter SI.Frequency fSource=50 "Source frequency"
7:     annotation(Dialog(group="Source"));
8:   parameter SI.Resistance RLoad=10 "Load resistance of source"
9:     annotation(Dialog(group="Source"));
10:   parameter SI.Resistance RGround=100e3 "Resistance of ground connection"
11:     annotation(Dialog(group="Source"));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/67269a20a4f821a5.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
