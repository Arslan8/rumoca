# FINDING-02133: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL |
| Target | smee.Lmd |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smee-dol-smee-lmd-unbounded.md](../../v2/bugs/FINDING-smee-dol-smee-lmd-unbounded.md) — reviewed as `FINDING-02133-smee-dol-smee-lmd.md`, which a later run renamed |
| Original SHA-256 | f947c076d391492c92cb4d372a71954048d8f57ff7b9dc3b553e7293da0d5ddf |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo:48`. Role: `parameter`; binding: `smeeData.Lmd`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo — source snapshot](../evidence/sources/3bf26424ac9fce16-SM_ElectricalExcited.mo)

```modelica
46:       Dialog(group="Operational temperatures", enable=not useThermalPort
47:            and useDamperCage));
48:   parameter SI.Inductance Lmd(start=1.5*ZsRef/(2*pi*fsNominal))
49:     "Stator main field inductance per phase in d-axis"
50:     annotation (Dialog(tab="Nominal resistances and inductances"));
51:   parameter SI.Inductance Lmq(start=1.5*ZsRef/(2*pi*fsNominal))
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/60c0c577a4240961.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
