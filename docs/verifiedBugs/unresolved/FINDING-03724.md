# FINDING-03724: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.QuadraticCoreAirgap |
| Target | delta |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-03724-quadraticcoreairgap-delta.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | db9309083c0f5c98fd903b4ff36f340559d427754396c566b37831ead484b67a |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/FluxTubes/Examples/BasicExamples/QuadraticCoreAirgap.mo:7`. Role: `parameter`; binding: `0.001`; effective min: `None`; effective max: `None`. 

[Magnetic/FluxTubes/Examples/BasicExamples/QuadraticCoreAirgap.mo — source snapshot](../evidence/sources/1c49afa437b0eb6f-QuadraticCoreAirgap.mo)

```modelica
5:   parameter SI.Length a=0.01 "Side length of square cross section";
6:   parameter Real mu_r=1000 "Relative permeability of core";
7:   parameter SI.Length delta=0.001 "Length of airgap";
8:   parameter Real sigma=0.1 "Leakage coefficient";
9:   parameter Integer N=500 "Number of turns of exciting coil";
10:   parameter SI.Current I=1.5 "Maximum exciting current";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/2c1757c0e25514b8.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
