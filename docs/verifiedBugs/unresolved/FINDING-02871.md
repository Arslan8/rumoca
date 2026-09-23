# FINDING-02871: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.Transformers.Rectifier6pulse |
| Target | transformerData1.Z1ph |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-rectifier6pulse-transformerdata1-z1ph-intent.md](../../v2/bugs/FINDING-rectifier6pulse-transformerdata1-z1ph-intent.md) — reviewed as `FINDING-02871-rectifier6pulse-transformerdata1-z1ph.md`, which a later run renamed |
| Original SHA-256 | 4de597c1fd617b17067520ff17f4c159443ef0bb9266d960216e50a248d4e69b |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/TransformerData.mo:35`. Role: `parameter`; binding: `(((0.5 * transformerData1.v_sc) * transformerData1.V1ph) / transformerData1.I1ph)`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/TransformerData.mo — source snapshot](../evidence/sources/aa784a3e208d0a32-TransformerData.mo)

```modelica
33:   final parameter SI.Current I2ph=SNominal/(3*V2ph)
34:     "Secondary phase current (RMS)";
35:   final parameter SI.Impedance Z1ph=0.5*v_sc*V1ph/I1ph
36:     "Primary impedance per phase";
37:   parameter SI.Resistance R1=0.5*P_sc/(3*I1ph^2)
38:     "Warm primary resistance per phase"
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/0eca3b9c4002495a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
