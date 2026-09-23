# FINDING-02209: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator |
| Target | smee.Rrd |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smee-generator-smee-rrd-unbounded.md](../../v2/bugs/FINDING-smee-generator-smee-rrd-unbounded.md) — reviewed as `FINDING-02209-smee-generator-smee-rrd.md`, which a later run renamed |
| Original SHA-256 | 549d2422f5be47cf1088ef0f94ad21131bd8c0c362679717ac5434e8b90aec5d |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo:68`. Role: `parameter`; binding: `smeeData.Rrd`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/SynchronousMachines/SM_ElectricalExcited.mo — source snapshot](../evidence/sources/3bf26424ac9fce16-SM_ElectricalExcited.mo)

```modelica
66:       group="Damper cage",
67:       enable=useDamperCage));
68:   parameter SI.Resistance Rrd(start=0.04*ZsRef)
69:     "Damper resistance in d-axis at TRef" annotation (Dialog(
70:       tab="Nominal resistances and inductances",
71:       group="Damper cage",
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/4d376a5cb19be7de.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
