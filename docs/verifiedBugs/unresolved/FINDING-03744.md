# FINDING-03744: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.ToroidalCoreAirgap |
| Target | delta |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-03744-toroidalcoreairgap-delta.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 4b902fd23aa9859d8e86cf9950fd79b8f2324b830a7da9602eb5102da3f272ee |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/FluxTubes/Examples/BasicExamples/ToroidalCoreAirgap.mo:8`. Role: `parameter`; binding: `0.001`; effective min: `None`; effective max: `None`. 

[Magnetic/FluxTubes/Examples/BasicExamples/ToroidalCoreAirgap.mo — source snapshot](../evidence/sources/cc0ac16d1e52a00d-ToroidalCoreAirgap.mo)

```modelica
6:   parameter SI.Length d=0.01 "Diameter of cylindrical cross section";
7:   parameter SI.RelativePermeability mu_r=1000 "Relative permeability of core";
8:   parameter SI.Length delta=0.001 "Length of airgap";
9:   parameter SI.Angle alpha=(1 - delta/(2*pi*r))*2*pi "Section angle of toroidal core";
10:   parameter Integer N=500 "Number of exciting coil turns";
11:   parameter SI.Current I=1.5 "Maximum exciting current";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/1d64eb2e38094351.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
