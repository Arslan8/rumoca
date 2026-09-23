# FINDING-00311: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.HeatingPNP_NORGate |
| Target | CapVal |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-heatingpnp-norgate-capval-zerolimit.md](../../v2/bugs/FINDING-heatingpnp-norgate-capval-zerolimit.md) — reviewed as `FINDING-00311-heatingpnp-norgate-capval.md`, which a later run renamed |
| Original SHA-256 | 9b547633648d1cb6de8169b88fd7e3a2d3eb75c7da1257ec75ed969234f7330d |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/HeatingPNP_NORGate.mo:4`. Role: `parameter`; binding: `0`; effective min: `0`; effective max: `None`. 

[Electrical/Analog/Examples/HeatingPNP_NORGate.mo — source snapshot](../evidence/sources/78b88eadab43219a-HeatingPNP_NORGate.mo)

```modelica
2: model HeatingPNP_NORGate "Heating PNP NOR Gate"
3:   extends Modelica.Icons.Example;
4:   parameter SI.Capacitance CapVal=0 "Value for capacitances" annotation (Evaluate=true);
5:   parameter SI.Time tauVal=0 "Value for ideal forward and reverse transit time of semiconductors" annotation (Evaluate=true);
6: 
7:   Modelica.Thermal.HeatTransfer.Components.HeatCapacitor HeatCapacitor1(C=0.1)
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f11c770db9a26ad4.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
