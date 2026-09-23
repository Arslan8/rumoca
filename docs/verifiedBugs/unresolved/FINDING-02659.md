# FINDING-02659: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.Transformers.AsymmetricalLoad |
| Target | RL |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-asymmetricalload-rl-zerolimit.md](../../v2/bugs/FINDING-asymmetricalload-rl-zerolimit.md) — reviewed as `FINDING-02659-asymmetricalload-rl.md`, which a later run renamed |
| Original SHA-256 | a04fb02ab3686977bdd9ba54243f51efcd9dbaf312de30e8ed481d421813edf6 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/Transformers/AsymmetricalLoad.mo:4`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/Transformers/AsymmetricalLoad.mo — source snapshot](../evidence/sources/5db02ef94ad04a26-AsymmetricalLoad.mo)

```modelica
2: model AsymmetricalLoad "Asymmetrical load"
3:   extends Modelica.Icons.Example;
4:   parameter SI.Resistance RL=1 "Load resistance";
5:   Modelica.Electrical.Polyphase.Sources.SineVoltage source(f=fill(
6:         50, 3), V=fill(sqrt(2/3)*100, 3)) annotation (Placement(
7:         transformation(
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/9b0b7f4a290b32fb.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
