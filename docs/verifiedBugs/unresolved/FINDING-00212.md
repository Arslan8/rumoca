# FINDING-00212: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.DemoPowerSupply |
| Target | conductor.T_ref |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-00212-demopowersupply-conductor-t-ref.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | c5f3e321d67d814465ea05b4086b1a5cb75684fdf6191edeee557e73965b7980 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Basic/VariableConductor.mo:4`. Role: `parameter`; binding: `300.15`; effective min: `0.0`; effective max: `None`. 

[Electrical/Analog/Basic/VariableConductor.mo — source snapshot](../evidence/sources/e1b2404e28f8726a-VariableConductor.mo)

```modelica
2: model VariableConductor
3:   "Ideal linear electrical conductor with variable conductance"
4:   parameter SI.Temperature T_ref=300.15 "Reference temperature";
5:   parameter SI.LinearTemperatureCoefficient alpha=0
6:     "Temperature coefficient of conductance (G_actual = G/(1 + alpha*(T_heatPort - T_ref))";
7:   extends Modelica.Electrical.Analog.Interfaces.OnePort;
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/ff588fc0bb00e857.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
