# FINDING-02919: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.Transformers.TransformerTestbench |
| Target | transformer.VectorGroup |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-02919-transformertestbench-transformer-vectorgroup.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 42b7d96fd7dade6bcbfb151615a60738e4f45b7ef4e4116c3e1b5a8bb2c589d0 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Interfaces/PartialBasicTransformer.mo:6`. Role: `constant`; binding: `'Dy01'`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Interfaces/PartialBasicTransformer.mo — source snapshot](../evidence/sources/00c574760d653f0d-PartialBasicTransformer.mo)

```modelica
4:   extends Machines.Icons.TransientTransformer;
5:   final parameter Integer m(min=1) = 3 "Number of phases" annotation(Evaluate=true);
6:   constant String VectorGroup="Yy00";
7:   parameter Real n(start=1)
8:     "Ratio primary voltage (line-to-line) / secondary voltage (line-to-line)";
9:   parameter SI.Resistance R1(start=5E-3/(if C1 == "D" then 1
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/349f88e4acab29ef.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
