# FINDING-03749: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.ToroidalCoreAirgap |
| Target | r |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-toroidalcoreairgap-r-divzero-2.md](../../v2/bugs/FINDING-toroidalcoreairgap-r-divzero-2.md) — reviewed as `FINDING-03749-toroidalcoreairgap-r.md`, which a later run renamed |
| Original SHA-256 | 5eec6f07912cad9dcbe6e2726fa8f5bb63548239802f67499e8073c43a8a60e0 |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/FluxTubes/Examples/BasicExamples/ToroidalCoreAirgap.mo:5`. Role: `parameter`; binding: `0.05`; effective min: `None`; effective max: `None`. 

[Magnetic/FluxTubes/Examples/BasicExamples/ToroidalCoreAirgap.mo — source snapshot](../evidence/sources/cc0ac16d1e52a00d-ToroidalCoreAirgap.mo)

```modelica
3:   extends Modelica.Icons.Example;
4:   import Modelica.Constants.pi;
5:   parameter SI.Length r=0.05 "Middle radius of iron core";
6:   parameter SI.Length d=0.01 "Diameter of cylindrical cross section";
7:   parameter SI.RelativePermeability mu_r=1000 "Relative permeability of core";
8:   parameter SI.Length delta=0.001 "Length of airgap";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/1d64eb2e38094351.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
