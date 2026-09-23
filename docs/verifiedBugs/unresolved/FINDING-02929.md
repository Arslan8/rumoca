# FINDING-02929: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Polyphase.Examples.Rectifier |
| Target | Ron |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-rectifier-ron-ruleoff-2.md](../../v2/bugs/FINDING-rectifier-ron-ruleoff-2.md) — reviewed as `FINDING-02929-rectifier-ron.md`, which a later run renamed |
| Original SHA-256 | 5b7cb35b4452aba696e41d1737d4dec0d1e65a51c9b46338b7b98f9605777b15 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Polyphase/Examples/Rectifier.mo:12`. Role: `parameter`; binding: `1e-05`; effective min: `None`; effective max: `None`. 

[Electrical/Polyphase/Examples/Rectifier.mo — source snapshot](../evidence/sources/7a36647d5ad00848-Rectifier.mo)

```modelica
10:   parameter SI.Capacitance C=0.005 "Total DC-Capacitance";
11:   parameter SI.Resistance RE=1E6 "Earthing Resistance";
12:   parameter SI.Resistance Ron=1e-5 "Closed diode resistance";
13:   parameter SI.Conductance Goff=1e-5
14:     "Opened diode conductance";
15:   parameter SI.Voltage Vknee=0 "Threshold diode voltage";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/bd2246d747d29983.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
