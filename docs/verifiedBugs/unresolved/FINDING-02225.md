# FINDING-02225: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator |
| Target | smeeData.Rrd |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smee-generator-smeedata-rrd-intent.md](../../v2/bugs/FINDING-smee-generator-smeedata-rrd-intent.md) — reviewed as `FINDING-02225-smee-generator-smeedata-rrd.md`, which a later run renamed |
| Original SHA-256 | 10453bf73afd3f9cf4069f00f311fda416fbe1c4bc2bee617da533b800797258 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/SynchronousMachineData.mo:113`. Role: `parameter`; binding: `Modelica.Electrical.Machines.Thermal.convertResistance((smeeData.rrd * smeeData.ZReference), smeeData.TrSpecification, smeeData.alpha20r, smeeData.TrRef)`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/SynchronousMachineData.mo — source snapshot](../evidence/sources/16b4341f9d5ec816-SynchronousMachineData.mo)

```modelica
111:       omega "Damper stray inductance in q-axis"
112:     annotation (Dialog(tab="Result", enable=false));
113:   parameter SI.Resistance Rrd=
114:       Machines.Thermal.convertResistance(
115:           rrd*ZReference,
116:           TrSpecification,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/4d376a5cb19be7de.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
