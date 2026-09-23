# FINDING-04626: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Thermal.FluidHeatFlow.Examples.PumpAndValve |
| Target | valve.dp0 |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-pumpandvalve-valve-dp0-divzero.md](../../v2/bugs/FINDING-pumpandvalve-valve-dp0-divzero.md) — reviewed as `FINDING-04626-pumpandvalve-valve-dp0.md`, which a later run renamed |
| Original SHA-256 | b1a746e9d1c67cdc4c96c924ff1ba72fe9a4acaa80c3e17a4ce7143075ce3ae5 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Thermal/FluidHeatFlow/Components/Valve.mo:17`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Thermal/FluidHeatFlow/Components/Valve.mo — source snapshot](../evidence/sources/fa143f27d1541dc3-Valve.mo)

```modelica
15:     "Leakage flow / max.flow @ y = 0"
16:     annotation(Dialog(group="Standard characteristic"));
17:   parameter SI.Pressure dp0(start=1) "Standard pressure drop"
18:     annotation(Dialog(group="Standard characteristic"));
19:   parameter SI.Density rho0(start=10)
20:     "Standard medium's density"
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/db1c40a3e361d88f.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
