# FINDING-04615: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Thermal.FluidHeatFlow.Examples.PumpAndValve |
| Target | valve.rho0 |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-pumpandvalve-valve-rho0-bound.md](../../v2/bugs/FINDING-pumpandvalve-valve-rho0-bound.md) — reviewed as `FINDING-04615-pumpandvalve-valve-rho0.md`, which a later run renamed |
| Original SHA-256 | f4193220e0bfa8d13da8b863489127ae031dca7338f9ac87282b62714b670083 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Thermal/FluidHeatFlow/Components/Valve.mo:19`. Role: `parameter`; binding: `10`; effective min: `0.0`; effective max: `None`. 

[Thermal/FluidHeatFlow/Components/Valve.mo — source snapshot](../evidence/sources/fa143f27d1541dc3-Valve.mo)

```modelica
17:   parameter SI.Pressure dp0(start=1) "Standard pressure drop"
18:     annotation(Dialog(group="Standard characteristic"));
19:   parameter SI.Density rho0(start=10)
20:     "Standard medium's density"
21:     annotation(Dialog(group="Standard characteristic"));
22:   parameter Real frictionLoss(min=0, max=1, start=0)
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/db1c40a3e361d88f.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
