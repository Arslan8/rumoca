# FINDING-00350: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.HeatingRectifier |
| Target | HeatingDiode1.R |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-heatingrectifier-heatingdiode1-r-divzero.md](../../v2/bugs/FINDING-heatingrectifier-heatingdiode1-r-divzero.md) — reviewed as `FINDING-00350-heatingrectifier-heatingdiode1-r.md`, which a later run renamed |
| Original SHA-256 | 829a4bf37fafd1070e0f52fe757923160f38721775b30030f344be022bee86f1 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Semiconductors/Diode.mo:8`. Role: `parameter`; binding: `100000000.0`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Semiconductors/Diode.mo — source snapshot](../evidence/sources/c1d36d6106513b1d-Diode.mo)

```modelica
6:   parameter SI.Voltage Vt=0.04 "Voltage equivalent of temperature (kT/qn)" annotation(Dialog(enable=not useTemperatureDependency));
7:   parameter Real Maxexp(final min=Modelica.Constants.small) = 15 "Max. exponent for linear continuation";
8:   parameter SI.Resistance R=1e8 "Parallel ohmic resistance";
9:   parameter Real EG=1.11 "Activation energy" annotation(Dialog(enable=useTemperatureDependency));
10:   parameter Real N=1 "Emission coefficient" annotation(Dialog(enable=useTemperatureDependency));
11:   parameter SI.Temperature TNOM=300.15 "Parameter measurement temperature" annotation(Dialog(enable=useTemperatureDependency));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/2d4a3f2cdd95ad4e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
