# FINDING-00243: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.DifferenceAmplifier |
| Target | Transistor2.Tr.NR |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-00243-differenceamplifier-transistor2-tr-nr.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 9c4c57f794fe32812c8e304f13b2e8a8e4a505089ac68acdc7af69c53121c3c6 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Semiconductors/NPN.mo:27`. Role: `parameter`; binding: `1.0`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Semiconductors/NPN.mo — source snapshot](../evidence/sources/b1769ee9ceb1f5f0-NPN.mo)

```modelica
25:   parameter SI.Voltage EG=1.11 "Energy gap for temperature effect on Is" annotation(Dialog(enable=useTemperatureDependency));
26:         parameter Real NF=1.0 "Forward current emission coefficient";
27:         parameter Real NR=1.0 "Reverse current emission coefficient";
28:   parameter SI.Voltage IC=0 "Initial value of collector to substrate voltage" annotation(Dialog(enable=UIC));
29:   parameter Boolean UIC = false "Decision if initial value IC should be used";
30:   parameter Boolean useSubstrate = false "= false, if substrate is implicitly grounded";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/a3f2f2f9a1ca72bf.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
