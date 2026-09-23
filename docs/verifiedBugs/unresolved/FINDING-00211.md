# FINDING-00211: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.DemoPowerSupply |
| Target | conductor.alpha |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-demopowersupply-conductor-alpha-divguarded.md](../../v2/bugs/FINDING-demopowersupply-conductor-alpha-divguarded.md) — reviewed as `FINDING-00211-demopowersupply-conductor-alpha.md`, which a later run renamed |
| Original SHA-256 | 040da1d7b3c438a68f4490a5a40297abd1758b7657ac61b4bf330c31eb16512b |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Basic/VariableConductor.mo:5`. Role: `parameter`; binding: `0`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Basic/VariableConductor.mo — source snapshot](../evidence/sources/e1b2404e28f8726a-VariableConductor.mo)

```modelica
3:   "Ideal linear electrical conductor with variable conductance"
4:   parameter SI.Temperature T_ref=300.15 "Reference temperature";
5:   parameter SI.LinearTemperatureCoefficient alpha=0
6:     "Temperature coefficient of conductance (G_actual = G/(1 + alpha*(T_heatPort - T_ref))";
7:   extends Modelica.Electrical.Analog.Interfaces.OnePort;
8:   extends Modelica.Electrical.Analog.Interfaces.ConditionalHeatPort(T=T_ref);
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/ff588fc0bb00e857.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
