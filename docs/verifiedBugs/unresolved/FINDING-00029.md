# FINDING-00029: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.CauerLowPassAnalog |
| Target | c3 |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-cauerlowpassanalog-c3-zerolimit.md](../../v2/bugs/FINDING-cauerlowpassanalog-c3-zerolimit.md) — reviewed as `FINDING-00029-cauerlowpassanalog-c3.md`, which a later run renamed |
| Original SHA-256 | 8e70ace1f41fa4466b3eeadba590f3f42d46e04d80f60326c8803d1414c183bc |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/CauerLowPassAnalog.mo:10`. Role: `parameter`; binding: `1.682`; effective min: `0`; effective max: `None`. 

[Electrical/Analog/Examples/CauerLowPassAnalog.mo — source snapshot](../evidence/sources/266c7b9da804f58a-CauerLowPassAnalog.mo)

```modelica
8:   parameter SI.Capacitance c2=1/(1.704992^2*l1)
9:     "Filter coefficient c2";
10:   parameter SI.Capacitance c3=1.682 "Filter coefficient c3";
11:   parameter SI.Capacitance c4=1/(1.179945^2*l2)
12:     "Filter coefficient c4";
13:   parameter SI.Capacitance c5=0.7262 "Filter coefficient c5";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/8dc1ee2bed892fd2.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
