# FINDING-02634: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_Inverter |
| Target | smr.Rrq |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smr-inverter-smr-rrq-unbounded.md](../../v2/bugs/FINDING-smr-inverter-smr-rrq-unbounded.md) — reviewed as `FINDING-02634-smr-inverter-smr-rrq.md`, which a later run renamed |
| Original SHA-256 | 26e8f571b34282a39f8b116612eb0901f07a6f9e6f56df932d7ed6bf8c17bc66 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/SynchronousMachines/SM_ReluctanceRotor.mo:67`. Role: `parameter`; binding: `smrData.Rrq`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/SynchronousMachines/SM_ReluctanceRotor.mo — source snapshot](../evidence/sources/0b2e3b8cab9dbfda-SM_ReluctanceRotor.mo)

```modelica
65:       group="Damper cage",
66:       enable=useDamperCage));
67:   parameter SI.Resistance Rrq=Rrd
68:     "Damper resistance in q-axis at TRef" annotation (Dialog(
69:       tab="Nominal resistances and inductances",
70:       group="Damper cage",
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/cf686768707ef1f9.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
