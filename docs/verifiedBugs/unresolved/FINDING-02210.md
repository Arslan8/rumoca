# FINDING-02210: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator |
| Target | smee.Rrq |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smee-generator-smee-rrq-unbounded.md](../../v2/bugs/FINDING-smee-generator-smee-rrq-unbounded.md) — reviewed as `FINDING-02210-smee-generator-smee-rrq.md`, which a later run renamed |
| Original SHA-256 | 52132f481a7175fc0c75855822161465a66e1dccc3b5fd584240851f34e31294 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo:73`. Role: `parameter`; binding: `smeeData.Rrq`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo — source snapshot](../evidence/sources/3bf26424ac9fce16-SM_ElectricalExcited.mo)

```modelica
71:       group="Damper cage",
72:       enable=useDamperCage));
73:   parameter SI.Resistance Rrq=Rrd
74:     "Damper resistance in q-axis at TRef" annotation (Dialog(
75:       tab="Nominal resistances and inductances",
76:       group="Damper cage",
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/4d376a5cb19be7de.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
