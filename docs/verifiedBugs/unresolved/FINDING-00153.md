# FINDING-00153: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.CauerLowPassSC |
| Target | l2 |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-cauerlowpasssc-l2-divzero-2.md](../../v2/bugs/FINDING-cauerlowpasssc-l2-divzero-2.md) — reviewed as `FINDING-00153-cauerlowpasssc-l2.md`, which a later run renamed |
| Original SHA-256 | c5432cdf3981095d9d358409ccb4d1c3691f512a33e7afd2e43a635621a39019 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/CauerLowPassSC.mo:6`. Role: `parameter`; binding: `0.8586`; effective min: `0`; effective max: `None`. 

[Electrical/Analog/Examples/CauerLowPassSC.mo — source snapshot](../evidence/sources/1f2741d02d1975f9-CauerLowPassSC.mo)

```modelica
4: 
5:   parameter SI.Capacitance l1=1.304 "Filter coefficient i1";
6:   parameter SI.Capacitance l2=0.8586 "Filter coefficient i2";
7:   parameter SI.Capacitance c1=1.072 "Filter coefficient c1";
8:   parameter SI.Capacitance c2=1/(1.704992^2*l1)
9:     "Filter coefficient c2";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f208d9a532ab730d.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
