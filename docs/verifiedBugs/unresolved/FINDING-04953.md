# FINDING-04953: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | ModelicaTest.Magnetic.FluxTubes.BasicComponents |
| Target | converter1.A |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-basiccomponents-converter1-a-zerolimit.md](../../v2/bugs/FINDING-basiccomponents-converter1-a-zerolimit.md) — reviewed as `FINDING-04953-basiccomponents-converter1-a.md`, which a later run renamed |
| Original SHA-256 | ef663ebbf262fb79606ed31c57078421a118f4e676f368ca9ce4f1d8ce93f650 |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/FluxTubes/Basic/ElectroMagneticConverterWithLeakageInductance.mo:28`. Role: `parameter`; binding: `1e-05`; effective min: `None`; effective max: `None`. 

[Magnetic/FluxTubes/Basic/ElectroMagneticConverterWithLeakageInductance.mo — source snapshot](../evidence/sources/6ba82a32cd763ca9-ElectroMagneticConverterWithLeakageInductance.mo)

```modelica
26:   parameter SI.Length L=10e-3 "Length in direction of flux"
27:     annotation (Dialog(tab="Leakage inductance"));
28:   parameter SI.Area A=10e-6 "Area of cross-section"
29:     annotation (Dialog(tab="Leakage inductance"));
30:   parameter SI.RelativePermeability mu_rel(min=Modelica.Constants.eps) = 1
31:     "Constant relative permeability of leakage inductance (> 0 required)"
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/8b65c0fbcd134e6c.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
