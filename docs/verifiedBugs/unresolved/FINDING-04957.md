# FINDING-04957: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | ModelicaTest.Magnetic.FluxTubes.BasicComponents |
| Target | converter1.eps |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-04957-basiccomponents-converter1-eps.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 39146c7181312ba2242d6d76ee2163404e34167c55a5470f59ca5a3ef5602064 |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/FluxTubes/Basic/ElectroMagneticConverterWithLeakageInductance.mo:41`. Role: `constant`; binding: `(100 * 2.220446049250313e-16)`; effective min: `None`; effective max: `None`. 

[Magnetic/FluxTubes/Basic/ElectroMagneticConverterWithLeakageInductance.mo — source snapshot](../evidence/sources/6ba82a32cd763ca9-ElectroMagneticConverterWithLeakageInductance.mo)

```modelica
39: 
40: protected
41:   constant Real eps=100*Modelica.Constants.eps;
42: equation
43:   v = p.v - n.v;
44:   0 = p.i + n.i;
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/8b65c0fbcd134e6c.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
