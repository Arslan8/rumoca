# FINDING-02897: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.Transformers.TransformerTestbench |
| Target | RL |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-transformertestbench-rl-ruleoff.md](../../v2/bugs/FINDING-transformertestbench-rl-ruleoff.md) — reviewed as `FINDING-02897-transformertestbench-rl.md`, which a later run renamed |
| Original SHA-256 | 31b97ef929c20398096bd50e8ccf5316275f5627b2f353362cd499463c56b083 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/Transformers/TransformerTestbench.mo:4`. Role: `parameter`; binding: `fill((1 / 3), 3)`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/Transformers/TransformerTestbench.mo — source snapshot](../evidence/sources/85b4b804d1f9c290-TransformerTestbench.mo)

```modelica
2: model TransformerTestbench "Transformer test bench"
3:   extends Modelica.Icons.Example;
4:   parameter SI.Resistance RL[3]=fill(1/3, 3)
5:     "Load resistance";
6:   Modelica.Electrical.Polyphase.Sources.SineVoltage source(f=fill(
7:         50, 3), V=fill(sqrt(2/3)*100, 3)) annotation (Placement(
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/349f88e4acab29ef.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
