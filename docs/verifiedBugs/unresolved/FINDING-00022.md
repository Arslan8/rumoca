# FINDING-00022: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Clocked.Examples.Systems.Utilities.ComponentsThrottleControl.ThrottleBody |
| Target | P_0 |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-throttlebody-p-0-divzero.md](../../v2/bugs/FINDING-throttlebody-p-0-divzero.md) — reviewed as `FINDING-00022-throttlebody-p-0.md`, which a later run renamed |
| Original SHA-256 | 6e2dd1c88c9b061e19eafbc1926bc94f10d5dcfa79b6aae036311c99550dab1a |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Clocked/Examples/Systems/Utilities/ComponentsThrottleControl/ThrottleBody.mo:5`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Clocked/Examples/Systems/Utilities/ComponentsThrottleControl/ThrottleBody.mo — source snapshot](../evidence/sources/a1c63f4d04e14d6d-ThrottleBody.mo)

```modelica
3:   extends Modelica.Blocks.Icons.Block;
4: 
5: parameter Modelica.Units.NonSI.Pressure_bar P_0 = 1 "Atmospheric pressure (bar)";
6: protected
7:   Real m_ai(start=0, fixed=true, unit="g") "Mass";
8:   Modelica.Units.NonSI.Angle_deg f_Theta "Auxiliary variable";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/496179f0b30d2f4e.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
