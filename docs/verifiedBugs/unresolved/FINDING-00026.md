# FINDING-00026: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.CauerLowPassAnalog |
| Target | l2 |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-cauerlowpassanalog-l2-unbounded.md](../../v2/bugs/FINDING-cauerlowpassanalog-l2-unbounded.md) — reviewed as `FINDING-00026-cauerlowpassanalog-l2.md`, which a later run renamed |
| Original SHA-256 | 6e7f587da34c060611b82ccc9d11ee134dd356a6300b91b324a9107c2b7d79ed |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/CauerLowPassAnalog.mo:6`. Role: `parameter`; binding: `0.8586`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/CauerLowPassAnalog.mo — source snapshot](../evidence/sources/266c7b9da804f58a-CauerLowPassAnalog.mo)

```modelica
4: 
5:   parameter SI.Inductance l1=1.304 "Filter coefficient I1";
6:   parameter SI.Inductance l2=0.8586 "Filter coefficient I2";
7:   parameter SI.Capacitance c1=1.072 "Filter coefficient c1";
8:   parameter SI.Capacitance c2=1/(1.704992^2*l1)
9:     "Filter coefficient c2";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/8dc1ee2bed892fd2.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
