# FINDING-01114: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.ControlledDCDrives.Utilities.IdealDcDc |
| Target | Td |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-01114-idealdcdc-td.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 0e4a48a234be0f6828606f75d2b4297b51b6f0a7e9c81a8fc3ab8f2a48a88982 |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/ControlledDCDrives/Utilities/IdealDcDc.mo:3`. Role: `parameter`; binding: `None`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/ControlledDCDrives/Utilities/IdealDcDc.mo — source snapshot](../evidence/sources/ba67317f59e09830-IdealDcDc.mo)

```modelica
1: within Modelica.Electrical.Machines.Examples.ControlledDCDrives.Utilities;
2: model IdealDcDc "Ideal DC-DC inverter"
3:   parameter SI.Time Td "Dead time";
4:   parameter SI.Time Ti=1e-6 "Time constant of integral power controller";
5:   Modelica.Electrical.Analog.Sources.SignalVoltage signalVoltage
6:     annotation (Placement(transformation(extent={{10,-80},{-10,-60}})));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/df2ac028c1bff7f7.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
