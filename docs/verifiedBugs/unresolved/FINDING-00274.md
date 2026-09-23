# FINDING-00274: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.HeatingMOSInverter |
| Target | H_NMOS.RDS |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-heatingmosinverter-h-nmos-rds-divzero.md](../../v2/bugs/FINDING-heatingmosinverter-h-nmos-rds-divzero.md) — reviewed as `FINDING-00274-heatingmosinverter-h-nmos-rds.md`, which a later run renamed |
| Original SHA-256 | e2c303b1857f551ac82a3e577a8b42bb55d3be553aa6360cb568c07808222d6d |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Semiconductors/NMOS.mo:20`. Role: `parameter`; binding: `10000000.0`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Semiconductors/NMOS.mo — source snapshot](../evidence/sources/d5a51528e9ae70f5-NMOS.mo)

```modelica
18:         parameter SI.Length dW=-2.5e-6 "Narrowing of channel";
19:         parameter SI.Length dL=-1.5e-6 "Shortening of channel";
20:         parameter SI.Resistance RDS=1e7 "Drain-Source-Resistance";
21:   parameter Boolean useTemperatureDependency = false "= true, if parameters Beta, K2 and Vt depend on temperature" annotation(Evaluate=true, HideResult=true, choices(checkBox=true));
22:   parameter SI.Temperature Tnom=300.15 "Parameter measurement temperature" annotation(Dialog(enable=useTemperatureDependency));
23:   parameter Real kvt=-6.96e-3 "Fitting parameter for Vt" annotation(Dialog(enable=useTemperatureDependency));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/acf8c02556f7d61b.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
