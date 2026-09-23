# FINDING-02206: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator |
| Target | smee.Lmq |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smee-generator-smee-lmq-intent.md](../../v2/bugs/FINDING-smee-generator-smee-lmq-intent.md) — reviewed as `FINDING-02206-smee-generator-smee-lmq.md`, which a later run renamed |
| Original SHA-256 | 3c7fdfbd089976e8cc5ad9c6722f3e950aea3e21ff348a3748c316795ff3576d |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo:51`. Role: `parameter`; binding: `smeeData.Lmq`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo — source snapshot](../evidence/sources/3bf26424ac9fce16-SM_ElectricalExcited.mo)

```modelica
49:     "Stator main field inductance per phase in d-axis"
50:     annotation (Dialog(tab="Nominal resistances and inductances"));
51:   parameter SI.Inductance Lmq(start=1.5*ZsRef/(2*pi*fsNominal))
52:     "Stator main field inductance per phase in q-axis"
53:     annotation (Dialog(tab="Nominal resistances and inductances"));
54:   parameter Boolean useDamperCage(start=true)
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/4d376a5cb19be7de.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
