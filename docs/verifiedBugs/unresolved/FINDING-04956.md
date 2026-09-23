# FINDING-04956: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | ModelicaTest.Magnetic.FluxTubes.BasicComponents |
| Target | eddyCurrent.R |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-basiccomponents-eddycurrent-r-unbounded.md](../../v2/bugs/FINDING-basiccomponents-eddycurrent-r-unbounded.md) — reviewed as `FINDING-04956-basiccomponents-eddycurrent-r.md`, which a later run renamed |
| Original SHA-256 | 01f37db206e19afaba69411792de09568d50b75e901f3ebf16d1c5f960f4b5bb |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/FluxTubes/Basic/EddyCurrent.mo:23`. Role: `parameter`; binding: `((eddyCurrent.rho * eddyCurrent.l) / eddyCurrent.A)`; effective min: `None`; effective max: `None`. 

[Magnetic/FluxTubes/Basic/EddyCurrent.mo — source snapshot](../evidence/sources/beb5cca17975c2ff-EddyCurrent.mo)

```modelica
21:     annotation(Dialog(enable=not useConductance));
22: 
23:   final parameter SI.Resistance R=rho*l/A
24:     "Electrical resistance of eddy current path"
25:     annotation(Dialog(enable=not useConductance));
26: 
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/8b65c0fbcd134e6c.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
