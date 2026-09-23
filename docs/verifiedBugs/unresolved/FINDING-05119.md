# FINDING-05119: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | NeuralPredatorPrey |
| Target | predatorEquilibrium |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-neuralpredatorprey-predatorequilibrium-divzero.md](../../v2/bugs/FINDING-neuralpredatorprey-predatorequilibrium-divzero.md) — reviewed as `FINDING-05119-neuralpredatorprey-predatorequilibrium.md`, which a later run renamed |
| Original SHA-256 | 1427262525dd37c00c59f53d2709df6836b3bff939509087945755123c4b3ac3 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `/data/mrumoca/rumoca/examples/models/NeuralPredatorPrey.mo:11`. Role: `parameter`; binding: `1.0`; effective min: `None`; effective max: `None`. 

[/data/mrumoca/rumoca/examples/models/NeuralPredatorPrey.mo — source snapshot](../evidence/sources/e05d7e768873dd0d-NeuralPredatorPrey.mo)

```modelica
9:     + nState * nHidden + nState;
10:   parameter Real preyEquilibrium = 1.0;
11:   parameter Real predatorEquilibrium = 1.0;
12:   parameter Real cycleGain = 1.25 "Predator-prey coupling around equilibrium";
13:   parameter Real seasonalGain = 0.18 "Seasonal perturbation strength";
14:   parameter Real seasonRate = 0.45 "Seasonal forcing frequency";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/dc1af8539fdb8ff7.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
