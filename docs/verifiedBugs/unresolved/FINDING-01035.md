# FINDING-01035: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.ThyristorBehaviourTest |
| Target | thyristor_v4_1.Roff |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-thyristorbehaviourtest-thyristor-v4-1-roff-unbounded.md](../../v2/bugs/FINDING-thyristorbehaviourtest-thyristor-v4-1-roff-unbounded.md) — reviewed as `FINDING-01035-thyristorbehaviourtest-thyristor-v4-1-roff.md`, which a later run renamed |
| Original SHA-256 | cded1a585b52bbf6a1e636590ce36a1c89914b4a014a62b5919d928c298aae03 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Semiconductors/Thyristor.mo:40`. Role: `parameter`; binding: `(((thyristor_v4_1.VDRM ^ 2) / thyristor_v4_1.VTM) / thyristor_v4_1.IH)`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Semiconductors/Thyristor.mo — source snapshot](../evidence/sources/dbc15414032e03ee-Thyristor.mo)

```modelica
38:   parameter SI.Resistance Ron=(VTM-0.7)/ITM
39:     "Forward conducting mode resistance";
40:   parameter SI.Resistance Roff=(VDRM^2)/VTM/IH
41:     "Blocking mode resistance";
42: 
43: equation
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f2dc7c4a18bb2bd2.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
