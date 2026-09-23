# FINDING-04954: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | ModelicaTest.Magnetic.FluxTubes.BasicComponents |
| Target | eddyCurrent.G |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-basiccomponents-eddycurrent-g-intent.md](../../v2/bugs/FINDING-basiccomponents-eddycurrent-g-intent.md) — reviewed as `FINDING-04954-basiccomponents-eddycurrent-g.md`, which a later run renamed |
| Original SHA-256 | 5c35100b41cf1d8f5ea33e145c7ec034d644691f996bd1f47c8055649b8cf2ca |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Magnetic/FluxTubes/Basic/EddyCurrent.mo:12`. Role: `parameter`; binding: `(1 / 9.8e-08)`; effective min: `0`; effective max: `None`. 

[Magnetic/FluxTubes/Basic/EddyCurrent.mo — source snapshot](../evidence/sources/beb5cca17975c2ff-EddyCurrent.mo)

```modelica
10:     "Use conductance instead of geometry data and rho"
11:     annotation(Evaluate=true, choices(checkBox=true));
12:   parameter SI.Conductance G(min=0) = 1/0.098e-6
13:     "Equivalent loss conductance G=A/rho/l"
14:     annotation(Dialog(enable=useConductance),Evaluate=true);
15:   parameter SI.Resistivity rho=0.098e-6
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/8b65c0fbcd134e6c.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
