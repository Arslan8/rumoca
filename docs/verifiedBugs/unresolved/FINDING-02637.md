# FINDING-02637: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMR_Inverter |
| Target | smr.damperCage.Rrd |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smr-inverter-smr-dampercage-rrd-zerolimit.md](../../v2/bugs/FINDING-smr-inverter-smr-dampercage-rrd-zerolimit.md) — reviewed as `FINDING-02637-smr-inverter-smr-dampercage-rrd.md`, which a later run renamed |
| Original SHA-256 | 0d49529c6c0f58bbb251c6c9757230f2a01f93fbf1f44c58d4c8b5bc5154e488 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/Components/DamperCage.mo:7`. Role: `parameter`; binding: `smrData.Rrd`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/Components/DamperCage.mo — source snapshot](../evidence/sources/a430d3c774d76eaf-DamperCage.mo)

```modelica
5:   parameter SI.Inductance Lrsigmaq
6:     "Stray inductance in q-axis per phase translated to stator";
7:   parameter SI.Resistance Rrd
8:     "Resistance in d-axis per phase translated to stator at T_ref";
9:   parameter SI.Resistance Rrq
10:     "Resistance in q-axis per phase translated to stator at T_ref";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/cf686768707ef1f9.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
