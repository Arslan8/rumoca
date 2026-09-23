# FINDING-00016: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Clocked.Examples.Systems.Utilities.ComponentsMixingUnit.MixingUnitWithContinuousControl |
| Target | c0 |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-00016-mixingunitwithcontinuouscontrol-c0.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 75194793ea4301330a1ffd08c73f1134e4db05ca3dafc39f0f85aa97211ad0de |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Clocked/Examples/Systems/Utilities/ComponentsMixingUnit/MixingUnitWithContinuousControl.mo:6`. Role: `parameter`; binding: `0.848`; effective min: `None`; effective max: `None`. 

[Clocked/Examples/Systems/Utilities/ComponentsMixingUnit/MixingUnitWithContinuousControl.mo — source snapshot](../evidence/sources/90aa2ee8b73d08de-MixingUnitWithContinuousControl.mo)

```modelica
4: 
5:   parameter SI.Frequency freq = 1/300 "Critical frequency of filter";
6:   parameter Real c0(unit="mol/l") = 0.848 "Nominal concentration";
7:   parameter SI.Temperature T0 = 308.5 "Nominal temperature";
8:   parameter Real a1_inv =  0.2674 "Process parameter of inverse plant model (see references in help)";
9:   parameter Real a21_inv = 1.815 "Process parameter of inverse plant model (see references in help)";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/4a214d5a5475e994.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
