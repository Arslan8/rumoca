# FINDING-02148: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL |
| Target | smeeData.Lssigma |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smee-dol-smeedata-lssigma-intent.md](../../v2/bugs/FINDING-smee-dol-smeedata-lssigma-intent.md) — reviewed as `FINDING-02148-smee-dol-smeedata-lssigma.md`, which a later run renamed |
| Original SHA-256 | c4047b82855c46c85fac61ae97ff49e5a8896b35014ce5e06c67da75d60d351d |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/SynchronousMachineData.mo:95`. Role: `parameter`; binding: `((smeeData.x0 * smeeData.ZReference) / smeeData.omega)`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/SynchronousMachineData.mo — source snapshot](../evidence/sources/16b4341f9d5ec816-SynchronousMachineData.mo)

```modelica
93:           TsRef) "Stator resistance per phase at TRef"
94:     annotation (Dialog(tab="Result", enable=false));
95:   parameter SI.Inductance Lssigma=x0*ZReference/omega
96:     "Stator stray inductance per phase"
97:     annotation (Dialog(tab="Result", enable=false));
98:   parameter Real ratioCommonStatorLeakage(final min=0, final max=1)=1
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/60c0c577a4240961.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
