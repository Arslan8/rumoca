# FINDING-02999: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.ACDC.Rectifier1Pulse.Thyristor1Pulse_R_Characteristic |
| Target | R |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-thyristor1pulse-r-characteristic-r-zerolimit.md](../../v2/bugs/FINDING-thyristor1pulse-r-characteristic-r-zerolimit.md) — reviewed as `FINDING-02999-thyristor1pulse-r-characteristic-r.md`, which a later run renamed |
| Original SHA-256 | 034eccbab5be0a7c8053787d49443bd28c6b09567984cd7f3eb9bc54e0c10ffc |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/Examples/ACDC/Rectifier1Pulse/Thyristor1Pulse_R_Characteristic.mo:8`. Role: `parameter`; binding: `20`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/Examples/ACDC/Rectifier1Pulse/Thyristor1Pulse_R_Characteristic.mo — source snapshot](../evidence/sources/95d87f1ddf3a877f-Thyristor1Pulse_R_Characteristic.mo)

```modelica
6:   extends Modelica.Icons.Example;
7:   import Modelica.Constants.pi;
8:   parameter SI.Resistance R=20 "Load resistance";
9:   Modelica.Electrical.Analog.Basic.Resistor resistor(R=R) annotation (
10:       Placement(transformation(
11:         origin={30,30},
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/e3326c370d0b1fe7.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
