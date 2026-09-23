# FINDING-00279: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.HeatingNPN_NORGate |
| Target | CapVal |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-heatingnpn-norgate-capval-zerolimit.md](../../v2/bugs/FINDING-heatingnpn-norgate-capval-zerolimit.md) — reviewed as `FINDING-00279-heatingnpn-norgate-capval.md`, which a later run renamed |
| Original SHA-256 | 2755ca35dd960db46b7f0e0c5c6f5ad2131cd0834c237af65f730517692899b8 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/HeatingNPN_NORGate.mo:4`. Role: `parameter`; binding: `0`; effective min: `0`; effective max: `None`. 

[Electrical/Analog/Examples/HeatingNPN_NORGate.mo — source snapshot](../evidence/sources/c5c190f3eca8a5e9-HeatingNPN_NORGate.mo)

```modelica
2: model HeatingNPN_NORGate "Heating NPN NOR Gate"
3:   extends Modelica.Icons.Example;
4:   parameter SI.Capacitance CapVal=0 "Value for capacitances" annotation(Evaluate=true);
5:   parameter SI.Time tauVal=0 "Value for ideal forward and reverse transit time of semiconductors"  annotation(Evaluate=true);
6: 
7:   Modelica.Thermal.HeatTransfer.Components.HeatCapacitor HeatCapacitor1(C=0.1)
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/6cb42ab3dab0120b.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
