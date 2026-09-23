# FINDING-01880: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_Transformer |
| Target | transformerData.Z1ph |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-transformer-transformerdata-z1ph-intent.md](../../v2/bugs/FINDING-imc-transformer-transformerdata-z1ph-intent.md) — reviewed as `FINDING-01880-imc-transformer-transformerdata-z1ph.md`, which a later run renamed |
| Original SHA-256 | 15545f17b3c53a81c086c02d24323d16317404f968eb217add683d24d5acb52a |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/TransformerData.mo:35`. Role: `parameter`; binding: `(((0.5 * transformerData.v_sc) * transformerData.V1ph) / transformerData.I1ph)`; effective min: `None`; effective max: `None`. 

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

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/ea078e37b0773dc4.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
