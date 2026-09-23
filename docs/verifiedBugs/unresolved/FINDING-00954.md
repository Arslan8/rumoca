# FINDING-00954: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.Rectifier |
| Target | LAC |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-rectifier-lac-zerolimit.md](../../v2/bugs/FINDING-rectifier-lac-zerolimit.md) — reviewed as `FINDING-00954-rectifier-lac.md`, which a later run renamed |
| Original SHA-256 | ca0493fd9c57bba9a472e6b125ea6720849e435d057d54f4b5f56a60cd577c82 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/Rectifier.mo:7`. Role: `parameter`; binding: `6e-05`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/Rectifier.mo — source snapshot](../evidence/sources/df3ae3151f74ba58-Rectifier.mo)

```modelica
5:   parameter SI.Voltage VAC=400 "RMS line-to-line";
6:   parameter SI.Frequency f=50 "Line frequency";
7:   parameter SI.Inductance LAC=60E-6 "Line inductor";
8:   parameter SI.Resistance Ron=1E-3 "Diode forward resistance";
9:   parameter SI.Conductance Goff=1E-3 "Diode backward conductance";
10:   parameter SI.Voltage Vknee=2 "Diode threshold voltage";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/c0679440dabef24f.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
