# FINDING-02151: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL |
| Target | smeeData.Lrsigmad |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smee-dol-smeedata-lrsigmad-intent.md](../../v2/bugs/FINDING-smee-dol-smeedata-lrsigmad-intent.md) — reviewed as `FINDING-02151-smee-dol-smeedata-lrsigmad.md`, which a later run renamed |
| Original SHA-256 | 921040f6fe5ab637249afe5c346a8510b691613cdba46a7079c6035cb37e92d1 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/SynchronousMachineData.mo:107`. Role: `parameter`; binding: `(((smeeData.xrd - smeeData.xmd) * smeeData.ZReference) / smeeData.omega)`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/SynchronousMachineData.mo — source snapshot](../evidence/sources/16b4341f9d5ec816-SynchronousMachineData.mo)

```modelica
105:     "Main field inductance per phase in q-axis"
106:     annotation (Dialog(tab="Result", enable=false));
107:   parameter SI.Inductance Lrsigmad=(xrd - xmd)*ZReference/
108:       omega "Damper stray inductance in d-axis"
109:     annotation (Dialog(tab="Result", enable=false));
110:   parameter SI.Inductance Lrsigmaq=(xrq - xmq)*ZReference/
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/60c0c577a4240961.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
