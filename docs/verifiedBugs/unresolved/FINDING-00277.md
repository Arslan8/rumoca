# FINDING-00277: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.HeatingMOSInverter |
| Target | H_NMOS.Tnom |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-heatingmosinverter-h-nmos-tnom-divunresolved.md](../../v2/bugs/FINDING-heatingmosinverter-h-nmos-tnom-divunresolved.md) — reviewed as `FINDING-00277-heatingmosinverter-h-nmos-tnom.md`, which a later run renamed |
| Original SHA-256 | 3f35578c3191009462b45b8b1762557a1b68a64e068513c1f3984af2e9ff7249 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Semiconductors/NMOS.mo:22`. Role: `parameter`; binding: `300.15`; effective min: `0.0`; effective max: `None`. 

[Electrical/Analog/Semiconductors/NMOS.mo — source snapshot](../evidence/sources/d5a51528e9ae70f5-NMOS.mo)

```modelica
20:         parameter SI.Resistance RDS=1e7 "Drain-Source-Resistance";
21:   parameter Boolean useTemperatureDependency = false "= true, if parameters Beta, K2 and Vt depend on temperature" annotation(Evaluate=true, HideResult=true, choices(checkBox=true));
22:   parameter SI.Temperature Tnom=300.15 "Parameter measurement temperature" annotation(Dialog(enable=useTemperatureDependency));
23:   parameter Real kvt=-6.96e-3 "Fitting parameter for Vt" annotation(Dialog(enable=useTemperatureDependency));
24:   parameter Real kk2=6e-4 "Fitting parameter for K2" annotation(Dialog(enable=useTemperatureDependency));
25:   extends Modelica.Electrical.Analog.Interfaces.ConditionalHeatPort(useHeatPort=useTemperatureDependency);
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/acf8c02556f7d61b.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
