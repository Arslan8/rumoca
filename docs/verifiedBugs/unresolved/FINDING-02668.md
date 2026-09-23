# FINDING-02668: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.Transformers.AsymmetricalLoad |
| Target | transformer.R2 |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-asymmetricalload-transformer-r2-ruleoff.md](../../v2/bugs/FINDING-asymmetricalload-transformer-r2-ruleoff.md) — reviewed as `FINDING-02668-asymmetricalload-transformer-r2.md`, which a later run renamed |
| Original SHA-256 | ac76572d6609145c883460e2ca6f52d97edce610ac2f33c58d565262a8ebd49d |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Interfaces/PartialBasicTransformer.mo:21`. Role: `parameter`; binding: `transformerData.R2`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Interfaces/PartialBasicTransformer.mo — source snapshot](../evidence/sources/00c574760d653f0d-PartialBasicTransformer.mo)

```modelica
19:          then 1 else 3)) "Primary stray inductance per phase"
20:     annotation (Dialog(tab="Nominal resistances and inductances"));
21:   parameter SI.Resistance R2(start=5E-3/(if C2 == "d" then 1
22:          else 3)) "Secondary resistance per phase at TRef"
23:     annotation (Dialog(tab="Nominal resistances and inductances"));
24:   parameter SI.Temperature T2Ref(start=293.15)
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/9b0b7f4a290b32fb.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
