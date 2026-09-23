# FINDING-02629: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_Inverter |
| Target | smr.Lmd |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smr-inverter-smr-lmd-intent.md](../../v2/bugs/FINDING-smr-inverter-smr-lmd-intent.md) — reviewed as `FINDING-02629-smr-inverter-smr-lmd.md`, which a later run renamed |
| Original SHA-256 | af55f9ad932607e49f76bb285b652f228b0c696c1e79a0e46c7426116a205395 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/SynchronousMachines/SM_ReluctanceRotor.mo:42`. Role: `parameter`; binding: `smrData.Lmd`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/SynchronousMachines/SM_ReluctanceRotor.mo — source snapshot](../evidence/sources/0b2e3b8cab9dbfda-SM_ReluctanceRotor.mo)

```modelica
40:       Dialog(group="Operational temperatures", enable=not useThermalPort
41:            and useDamperCage));
42:   parameter SI.Inductance Lmd(start=2.9*ZsRef/(2*pi*fsNominal))
43:     "Stator main field inductance per phase in d-axis"
44:     annotation (Dialog(tab="Nominal resistances and inductances"));
45:   parameter SI.Inductance Lmq(start=0.9*ZsRef/(2*pi*fsNominal))
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/cf686768707ef1f9.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
