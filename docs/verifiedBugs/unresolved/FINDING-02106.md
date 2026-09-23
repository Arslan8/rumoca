# FINDING-02106: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start |
| Target | aimsData.useTurnsRatio |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-02106-ims-start-aimsdata-useturnsratio.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 70d203aa121c89a41a9f615b09f9af9ae83c2d143e9dbddadbbd9aaade217e25 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/ParameterRecords/IM_SlipRingData.mo:28`. Role: `parameter`; binding: `True`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/ParameterRecords/IM_SlipRingData.mo — source snapshot](../evidence/sources/43598d6d883f8edf-IM_SlipRingData.mo)

```modelica
26:     "Temperature coefficient of rotor resistance at 20 degC"
27:     annotation (Dialog(tab="Nominal resistances and inductances"));
28:   parameter Boolean useTurnsRatio=true
29:     "Use turnsRatio or calculate from locked-rotor voltage?";
30:   parameter Real turnsRatio(final min=Modelica.Constants.small)=
31:     VsNominal/VrLockedRotor*(2*pi*fsNominal*Lm)/sqrt(Rs^2 + (2*pi*
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/2804e4f64ad6a33e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
