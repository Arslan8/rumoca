# FINDING-02155: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL |
| Target | smeeData.Re |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smee-dol-smeedata-re-zerolimit.md](../../v2/bugs/FINDING-smee-dol-smeedata-re-zerolimit.md) — reviewed as `FINDING-02155-smee-dol-smeedata-re.md`, which a later run renamed |
| Original SHA-256 | 6c8feca5ded6463fb56fccf22e5596a652cead25392f37b7ee210789c0745c81 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/SynchronousMachineData.mo:127`. Role: `parameter`; binding: `(((3 / 2) * (smeeData.turnsRatio ^ 2)) * Modelica.Electrical.Machines.Thermal.convertResistance((smeeData.re * smeeData.ZReference), smeeData.TeSpecification, smeeData.alpha20e, smeeData.TeRef))`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/SynchronousMachineData.mo — source snapshot](../evidence/sources/16b4341f9d5ec816-SynchronousMachineData.mo)

```modelica
125:           TrRef) "Damper resistance in q-axis at TRef"
126:     annotation (Dialog(tab="Result", enable=false));
127:   parameter SI.Resistance Re=3/2*turnsRatio^2*
128:       Machines.Thermal.convertResistance(
129:           re*ZReference,
130:           TeSpecification,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/60c0c577a4240961.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
