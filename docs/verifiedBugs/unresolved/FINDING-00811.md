# FINDING-00811: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.DifferentialAmplifier |
| Target | data.R4 |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-differentialamplifier-data-r4-zerolimit.md](../../v2/bugs/FINDING-differentialamplifier-data-r4-zerolimit.md) — reviewed as `FINDING-00811-differentialamplifier-data-r4.md`, which a later run renamed |
| Original SHA-256 | ea99623c57dc7b025030096caa547feef1018394b24222d4418a3044acdb2096 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/DifferentialAmplifierData.mo:24`. Role: `parameter`; binding: `data.R3`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/OpAmpCircuits/DifferentialAmplifierData.mo — source snapshot](../evidence/sources/0cea00d163c1f4d9-DifferentialAmplifierData.mo)

```modelica
22:   parameter SI.Resistance R3=R1/k "Resistor 3"
23:     annotation(Dialog(group="OpAmp"));
24:   parameter SI.Resistance R4=R3 "Resistor 4"
25:     annotation(Dialog(group="OpAmp"));
26:   parameter SI.Resistance RInstrument=100e3 "Input resistance of instrument"
27:     annotation(Dialog(group="Measurement"));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/67269a20a4f821a5.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
