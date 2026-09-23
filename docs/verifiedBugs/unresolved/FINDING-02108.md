# FINDING-02108: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start |
| Target | aimsData.VsNominal |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-02108-ims-start-aimsdata-vsnominal.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | be71f7d4e12895e6e90d42f685f49433e661cd6552e58fc7706775672d78c4a2 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/ParameterRecords/IM_SlipRingData.mo:35`. Role: `parameter`; binding: `100`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/ParameterRecords/IM_SlipRingData.mo — source snapshot](../evidence/sources/43598d6d883f8edf-IM_SlipRingData.mo)

```modelica
33:     "Effective number of stator turns / effective number of rotor turns"
34:     annotation (Dialog(enable=useTurnsRatio));
35:   parameter SI.Voltage VsNominal=100
36:     "Nominal stator voltage per phase"
37:     annotation (Dialog(enable=not useTurnsRatio));
38:   parameter SI.Voltage VrLockedRotor=100*(2*pi*fsNominal*Lm)
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/2804e4f64ad6a33e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
