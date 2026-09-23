# FINDING-02240: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_Generator |
| Target | smeeData.VsNominal |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-smee-generator-smeedata-vsnominal-divzero-2.md](../../v2/bugs/FINDING-smee-generator-smeedata-vsnominal-divzero-2.md) — reviewed as `FINDING-02240-smee-generator-smeedata-vsnominal.md`, which a later run renamed |
| Original SHA-256 | 22aafa5b6c1f0d24efadc6cd02b4f10394493c7b6e14bcf5598ed694338ae136 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/SynchronousMachineData.mo:8`. Role: `parameter`; binding: `100`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/SynchronousMachineData.mo — source snapshot](../evidence/sources/16b4341f9d5ec816-SynchronousMachineData.mo)

```modelica
6:   parameter SI.ApparentPower SNominal(start=30E3)
7:     "Nominal apparent power";
8:   parameter SI.Voltage VsNominal(start=100)
9:     "Nominal stator voltage per phase";
10:   final parameter SI.Current IsNominal=SNominal/(3*VsNominal)
11:     "Nominal stator current per phase";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/4d376a5cb19be7de.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
