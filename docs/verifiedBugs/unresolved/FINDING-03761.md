# FINDING-03761: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Magnetic.FluxTubes.Examples.BasicExamples.ToroidalCoreQuadraticCrossSection |
| Target | r_i |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-toroidalcorequadraticcrosssection-r-i-divzero-2.md](../../v2/bugs/FINDING-toroidalcorequadraticcrosssection-r-i-divzero-2.md) — reviewed as `FINDING-03761-toroidalcorequadraticcrosssection-r-i.md`, which a later run renamed |
| Original SHA-256 | 9c30f3c27d4c743bbe997a1202ba0b695fbba5ac2fbd9b9bbe46a05afc21a2db |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/FluxTubes/Examples/BasicExamples/ToroidalCoreQuadraticCrossSection.mo:7`. Role: `parameter`; binding: `0.045`; effective min: `None`; effective max: `None`. 

[Magnetic/FluxTubes/Examples/BasicExamples/ToroidalCoreQuadraticCrossSection.mo — source snapshot](../evidence/sources/ff86882d2c26beee-ToroidalCoreQuadraticCrossSection.mo)

```modelica
5:   import Modelica.Constants.pi;
6:   parameter SI.Length r_o=0.055 "Outer radius of iron core";
7:   parameter SI.Length r_i=0.045 "Inner radius of iron core";
8:   parameter SI.Length l=0.01 "Length of rectangular cross section";
9:   parameter SI.RelativePermeability mu_r=1000 "Relative permeability of core";
10:   parameter SI.Length delta=0.001 "Length of airgap";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/d344ac2d66511db7.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
