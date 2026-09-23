# FINDING-00237: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.DifferenceAmplifier |
| Target | Transistor1.Tr.Tnom |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-differenceamplifier-transistor1-tr-tnom-divzero.md](../../v2/bugs/FINDING-differenceamplifier-transistor1-tr-tnom-divzero.md) — reviewed as `FINDING-00237-differenceamplifier-transistor1-tr-tnom.md`, which a later run renamed |
| Original SHA-256 | 8f8b13e98835f9b65b27fb3219f400b2b35c01ee128fe0ec4315bda071b3296e |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Semiconductors/NPN.mo:22`. Role: `parameter`; binding: `300.15`; effective min: `0.0`; effective max: `None`. 

[Electrical/Analog/Semiconductors/NPN.mo — source snapshot](../evidence/sources/b1769ee9ceb1f5f0-NPN.mo)

```modelica
20:   parameter Boolean useTemperatureDependency = false "= true, if parameters Bf, Br, Is and Vt depend on temperature" annotation(Evaluate=true, HideResult=true, choices(checkBox=true));
21:   parameter SI.Voltage Vt=0.02585 "Voltage equivalent of temperature" annotation(Dialog(enable=not useTemperatureDependency));
22:   parameter SI.Temperature Tnom=300.15 "Parameter measurement temperature" annotation(Dialog(enable=useTemperatureDependency));
23:   parameter Real XTI=3 "Temperature exponent for effect on Is" annotation(Dialog(enable=useTemperatureDependency));
24:   parameter Real XTB=0 "Forward and reverse beta temperature exponent" annotation(Dialog(enable=useTemperatureDependency));
25:   parameter SI.Voltage EG=1.11 "Energy gap for temperature effect on Is" annotation(Dialog(enable=useTemperatureDependency));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/a3f2f2f9a1ca72bf.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
