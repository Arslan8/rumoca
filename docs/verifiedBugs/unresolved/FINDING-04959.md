# FINDING-04959: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | ModelicaTest.Magnetic.FluxTubes.BasicComponents |
| Target | eddyCurrent.l |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-04959-basiccomponents-eddycurrent-l.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 24163f8d0d7b3c85e622438722fcd82f09327e733283adc3c18da819dfb3174e |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/FluxTubes/Basic/EddyCurrent.mo:18`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Magnetic/FluxTubes/Basic/EddyCurrent.mo — source snapshot](../evidence/sources/beb5cca17975c2ff-EddyCurrent.mo)

```modelica
16:     "Resistivity of flux tube material (default: Iron at 20degC)"
17:     annotation(Dialog(enable=not useConductance));
18:   parameter SI.Length l=1 "Average length of eddy current path"
19:     annotation(Dialog(enable=not useConductance));
20:   parameter SI.Area A=1 "Cross sectional area of eddy current path"
21:     annotation(Dialog(enable=not useConductance));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/8b65c0fbcd134e6c.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
