# FINDING-04432: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Mechanics.Translational.Examples.EddyCurrentBrake |
| Target | eddyCurrentForce.TRef |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-04432-eddycurrentbrake-eddycurrentforce-tref.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 4b4cc3853f45935e8d8a2941aa4bf56d317ed5c17c6fe783dd08ca1e9f245f79 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Translational/Sources/EddyCurrentForce.mo:10`. Role: `parameter`; binding: `293.15`; effective min: `0.0`; effective max: `None`. 

[Mechanics/Translational/Sources/EddyCurrentForce.mo — source snapshot](../evidence/sources/002a973c5a08daf5-EddyCurrentForce.mo)

```modelica
8:   parameter SI.Velocity v_nominal(min=Modelica.Constants.eps)
9:     "Nominal speed (leads to maximum force) at reference temperature";
10:   parameter SI.Temperature TRef(start=293.15)
11:     "Reference temperature";
12:   parameter Modelica.Electrical.Machines.Thermal.LinearTemperatureCoefficient20
13:     alpha20(start=0) "Temperature coefficient of material";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/b7a045b48df79d60.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
