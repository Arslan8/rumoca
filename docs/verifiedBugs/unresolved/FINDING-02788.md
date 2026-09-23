# FINDING-02788: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.Transformers.Rectifier12pulse |
| Target | transformerData1.L2sigma |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-rectifier12pulse-transformerdata1-l2sigma-intent.md](../../v2/bugs/FINDING-rectifier12pulse-transformerdata1-l2sigma-intent.md) — reviewed as `FINDING-02788-rectifier12pulse-transformerdata1-l2sigma.md`, which a later run renamed |
| Original SHA-256 | 856a185348cc609e9565b392a10878fcdb41cfef09e1c9136b47ce28d7c1a779 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/TransformerData.mo:48`. Role: `parameter`; binding: `(sqrt(((transformerData1.Z2ph ^ 2) - (transformerData1.R2 ^ 2))) / ((2 * (2 * asin(1.0))) * transformerData1.f))`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/TransformerData.mo — source snapshot](../evidence/sources/aa784a3e208d0a32-TransformerData.mo)

```modelica
46:     "Warm secondary resistance per phase"
47:     annotation (Dialog(tab="Result",enable=false));
48:   parameter SI.Inductance L2sigma=sqrt(Z2ph^2 - R2^2)/(2*
49:       Modelica.Constants.pi*f) "Secondary stray inductance per phase"
50:     annotation (Dialog(tab="Result",enable=false));
51:   annotation (defaultComponentPrefixes="parameter",Documentation(info="<html>
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/2fadfbbc56888059.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
