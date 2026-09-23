# FINDING-02732: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.Transformers.IMC_Transformer |
| Target | transformerData.L1sigma |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-transformer-transformerdata-l1sigma-intent-2.md](../../v2/bugs/FINDING-imc-transformer-transformerdata-l1sigma-intent-2.md) — reviewed as `FINDING-02732-imc-transformer-transformerdata-l1sigma.md`, which a later run renamed |
| Original SHA-256 | 10fbf352df9eb305c5f516871b502d631f5639fdb9060287445d3a251908e744 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/TransformerData.mo:40`. Role: `parameter`; binding: `(sqrt(((transformerData.Z1ph ^ 2) - (transformerData.R1 ^ 2))) / ((2 * (2 * asin(1.0))) * transformerData.f))`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/TransformerData.mo — source snapshot](../evidence/sources/aa784a3e208d0a32-TransformerData.mo)

```modelica
38:     "Warm primary resistance per phase"
39:     annotation (Dialog(tab="Result",enable=false));
40:   parameter SI.Inductance L1sigma=sqrt(Z1ph^2 - R1^2)/(2*
41:       Modelica.Constants.pi*f) "Primary stray inductance per phase"
42:     annotation (Dialog(tab="Result",enable=false));
43:   final parameter SI.Impedance Z2ph=0.5*v_sc*V2ph/I2ph
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/1d64c76f1b77946f.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
