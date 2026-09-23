# FINDING-02902: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.Transformers.TransformerTestbench |
| Target | transformerData.Z2ph |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-transformertestbench-transformerdata-z2ph-intent.md](../../v2/bugs/FINDING-transformertestbench-transformerdata-z2ph-intent.md) — reviewed as `FINDING-02902-transformertestbench-transformerdata-z2ph.md`, which a later run renamed |
| Original SHA-256 | 4b7e8a18162e1f00b0b12756bbf640940287ba0f4e46574e9fd7c87e0830cc35 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/TransformerData.mo:43`. Role: `parameter`; binding: `(((0.5 * transformerData.v_sc) * transformerData.V2ph) / transformerData.I2ph)`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/TransformerData.mo — source snapshot](../evidence/sources/aa784a3e208d0a32-TransformerData.mo)

```modelica
41:       Modelica.Constants.pi*f) "Primary stray inductance per phase"
42:     annotation (Dialog(tab="Result",enable=false));
43:   final parameter SI.Impedance Z2ph=0.5*v_sc*V2ph/I2ph
44:     "Secondary impedance per phase";
45:   parameter SI.Resistance R2=0.5*P_sc/(3*I2ph^2)
46:     "Warm secondary resistance per phase"
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/349f88e4acab29ef.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
