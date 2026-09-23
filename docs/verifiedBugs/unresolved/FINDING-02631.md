# FINDING-02631: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_Inverter |
| Target | smr.Lrsigmad |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smr-inverter-smr-lrsigmad-intent.md](../../v2/bugs/FINDING-smr-inverter-smr-lrsigmad-intent.md) — reviewed as `FINDING-02631-smr-inverter-smr-lrsigmad.md`, which a later run renamed |
| Original SHA-256 | 2e51ee50c7c354732c68a66af4a5d5645c248d192e1c40b53300312fa5b47570 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/SynchronousMachines/SM_ReluctanceRotor.mo:51`. Role: `parameter`; binding: `smrData.Lrsigmad`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/SynchronousMachines/SM_ReluctanceRotor.mo — source snapshot](../evidence/sources/0b2e3b8cab9dbfda-SM_ReluctanceRotor.mo)

```modelica
49:     "Enable / disable damper cage" annotation (Evaluate=true, Dialog(tab=
50:           "Nominal resistances and inductances", group="Damper cage"));
51:   parameter SI.Inductance Lrsigmad(start=0.05*ZsRef/(2*pi*
52:         fsNominal)) "Damper stray inductance in d-axis" annotation (
53:       Dialog(
54:       tab="Nominal resistances and inductances",
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/cf686768707ef1f9.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
