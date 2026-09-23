# FINDING-01947: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_YDarc |
| Target | switchYDwithArc.idealCloser.Ron |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-imc-ydarc-switchydwitharc-idealcloser-ron-ruleoff.md](../../v2/bugs/FINDING-imc-ydarc-switchydwitharc-idealcloser-ron-ruleoff.md) — reviewed as `FINDING-01947-imc-ydarc-switchydwitharc-idealcloser-ron.md`, which a later run renamed |
| Original SHA-256 | af98e798ef9e6aa0dab7b635522b10a3d8e72fc7dfb315d6106e5f0728f36c09 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Polyphase/Ideal/CloserWithArc.mo:4`. Role: `parameter`; binding: `fill(switchYDwithArc.Ron, switchYDwithArc.m)`; effective min: `zeros(3)`; effective max: `None`. 

[Electrical/Polyphase/Ideal/CloserWithArc.mo — source snapshot](../evidence/sources/49b754fb33cb08d7-CloserWithArc.mo)

```modelica
2: model CloserWithArc "Polyphase closer with arc"
3:   extends Interfaces.TwoPlug;
4:   parameter SI.Resistance Ron[m](final min=zeros(m), start=
5:         fill(1e-5, m)) "Closed switch resistance";
6:   parameter SI.Conductance Goff[m](final min=zeros(m), start=
7:         fill(1e-5, m)) "Opened switch conductance";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/a03f73e52ba0cfd4.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
