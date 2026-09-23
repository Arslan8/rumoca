# FINDING-02667: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.Transformers.AsymmetricalLoad |
| Target | transformer.L1sigma |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-asymmetricalload-transformer-l1sigma-zerolimit.md](../../v2/bugs/FINDING-asymmetricalload-transformer-l1sigma-zerolimit.md) — reviewed as `FINDING-02667-asymmetricalload-transformer-l1sigma.md`, which a later run renamed |
| Original SHA-256 | 67c63a85311c92b2f999e807f80dd39d6341253c1422399ee46a8ffab299dd09 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Interfaces/PartialBasicTransformer.mo:18`. Role: `parameter`; binding: `transformerData.L1sigma`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Interfaces/PartialBasicTransformer.mo — source snapshot](../evidence/sources/00c574760d653f0d-PartialBasicTransformer.mo)

```modelica
16:     "Temperature coefficient of primary resistance at 20 degC"
17:     annotation (Dialog(tab="Nominal resistances and inductances"));
18:   parameter SI.Inductance L1sigma(start=78E-6/(if C1 == "D"
19:          then 1 else 3)) "Primary stray inductance per phase"
20:     annotation (Dialog(tab="Nominal resistances and inductances"));
21:   parameter SI.Resistance R2(start=5E-3/(if C2 == "d" then 1
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/9b0b7f4a290b32fb.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
