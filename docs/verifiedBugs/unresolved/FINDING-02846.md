# FINDING-02846: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.Transformers.Rectifier12pulse |
| Target | transformerData1.f |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-rectifier12pulse-transformerdata1-f-divzero-2.md](../../v2/bugs/FINDING-rectifier12pulse-transformerdata1-f-divzero-2.md) — reviewed as `FINDING-02846-rectifier12pulse-transformerdata1-f.md`, which a later run renamed |
| Original SHA-256 | 94030301f430a26c6160da861f7fa7f4b1d9b9940f0e23aea2231191417358db |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/TransformerData.mo:4`. Role: `parameter`; binding: `50`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/TransformerData.mo — source snapshot](../evidence/sources/aa784a3e208d0a32-TransformerData.mo)

```modelica
2: record TransformerData "Calculates Impedances from nominal values"
3:   extends Modelica.Icons.Record;
4:   parameter SI.Frequency f(start=50) "Nominal frequency";
5:   parameter SI.Voltage V1(start=100)
6:     "Primary nominal line-to-line voltage (RMS)";
7:   parameter String C1(start="Y") "Choose primary connection" annotation (
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/2fadfbbc56888059.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
