# FINDING-02925: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Polyphase.Examples.Rectifier |
| Target | L |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-rectifier-l-zerolimit.md](../../v2/bugs/FINDING-rectifier-l-zerolimit.md) — reviewed as `FINDING-02925-rectifier-l.md`, which a later run renamed |
| Original SHA-256 | 926ed11f33c8ee78589942a8fe1bd8c704e98d0953e8ff942f41b61224973c7f |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Polyphase/Examples/Rectifier.mo:8`. Role: `parameter`; binding: `0.0001`; effective min: `None`; effective max: `None`. 

[Electrical/Polyphase/Examples/Rectifier.mo — source snapshot](../evidence/sources/7a36647d5ad00848-Rectifier.mo)

```modelica
6:   parameter SI.Voltage V=100 "RMS of Star-Voltage";
7:   parameter SI.Frequency f=50 "Frequency";
8:   parameter SI.Inductance L=0.0001 "Line Inductance";
9:   parameter SI.Resistance RL=2 "Load Resistance";
10:   parameter SI.Capacitance C=0.005 "Total DC-Capacitance";
11:   parameter SI.Resistance RE=1E6 "Earthing Resistance";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/bd2246d747d29983.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
