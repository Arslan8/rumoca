# FINDING-01752: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMC_InverterDrive |
| Target | pwm.svPWM.f |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-imc-inverterdrive-pwm-svpwm-f-divzero.md](../../v2/bugs/FINDING-imc-inverterdrive-pwm-svpwm-f-divzero.md) — reviewed as `FINDING-01752-imc-inverterdrive-pwm-svpwm-f.md`, which a later run renamed |
| Original SHA-256 | 36c68e3687835e5bc6ff656e84ce4c2607fcae9569428ce030b7168b6d316383 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/DCAC/Control/SVPWM.mo:3`. Role: `parameter`; binding: `2000`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/DCAC/Control/SVPWM.mo — source snapshot](../evidence/sources/4ed327ecbdfb0f44-SVPWM.mo)

```modelica
1: within Modelica.Electrical.PowerConverters.DCAC.Control;
2: block SVPWM "Space vector pulse width modulation"
3:   parameter SI.Frequency f "Switching frequency";
4:   extends Modelica.Blocks.Interfaces.DiscreteBlock(final samplePeriod=1/f);
5:   import Modelica.Constants.small;
6:   import Modelica.Constants.eps;
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f1b3b20d1746a2aa.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
