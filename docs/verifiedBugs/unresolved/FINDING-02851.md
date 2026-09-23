# FINDING-02851: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.Transformers.Rectifier6pulse |
| Target | RL |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-rectifier6pulse-rl-zerolimit.md](../../v2/bugs/FINDING-rectifier6pulse-rl-zerolimit.md) — reviewed as `FINDING-02851-rectifier6pulse-rl.md`, which a later run renamed |
| Original SHA-256 | 229d8284976aa2e36ec0875a3c2d1beaf6a6d816adace4bb7dc4e4b57e48acb1 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/Transformers/Rectifier6pulse.mo:8`. Role: `parameter`; binding: `0.4`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/Transformers/Rectifier6pulse.mo — source snapshot](../evidence/sources/fed84f5c19aff646-Rectifier6pulse.mo)

```modelica
6:     "Amplitude of star-voltage";
7:   parameter SI.Frequency f=50 "Frequency";
8:   parameter SI.Resistance RL=0.4 "Load resistance";
9:   parameter SI.Capacitance C=0.005 "Total DC-capacitance";
10:   parameter SI.Voltage VC0=sqrt(3)*V
11:     "Initial voltage of capacitance";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/0eca3b9c4002495a.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
