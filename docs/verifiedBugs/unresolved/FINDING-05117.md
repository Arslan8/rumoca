# FINDING-05117: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | NeuralODETensor |
| Target | nState |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-05117-neuralodetensor-nstate.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 8e88d4af3e7790bc1a04503ddf1489bd9f78f49d14a3a8f32da90bc87da4c14a |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `/data/mrumoca/rumoca/examples/models/NeuralODETensor.mo:2`. Role: `parameter`; binding: `2`; effective min: `None`; effective max: `None`. 

[/data/mrumoca/rumoca/examples/models/NeuralODETensor.mo — source snapshot](../evidence/sources/f1e5fca9fcc28b91-NeuralODETensor.mo)

```modelica
1: model NeuralODETensor
2:   final parameter Integer nState = 2 "Latent state dimension";
3:   parameter Integer nHidden(min = 2) = 32
4:     "Hidden width; nHidden=314 gives about 100k trainable parameters";
5:   final parameter Integer trainableParams =
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/3869486d4c21d3a9.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
