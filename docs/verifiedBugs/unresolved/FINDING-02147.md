# FINDING-02147: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.SynchronousMachines.SMEE_DOL |
| Target | smeeData.Rs |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smee-dol-smeedata-rs-intent.md](../../v2/bugs/FINDING-smee-dol-smeedata-rs-intent.md) — reviewed as `FINDING-02147-smee-dol-smeedata-rs.md`, which a later run renamed |
| Original SHA-256 | c0ca5b133254679363bc016ecd180f7772354333557111196d145f07c240151f |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Utilities/SynchronousMachineData.mo:88`. Role: `parameter`; binding: `Modelica.Electrical.Machines.Thermal.convertResistance((smeeData.rs * smeeData.ZReference), smeeData.TsSpecification, smeeData.alpha20s, smeeData.TsRef)`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Utilities/SynchronousMachineData.mo — source snapshot](../evidence/sources/16b4341f9d5ec816-SynchronousMachineData.mo)

```modelica
86:   final parameter Real re=xe/(omega*Td0Transient)
87:     "Excitation resistance per phase at specification temperature [pu]";
88:   parameter SI.Resistance Rs=
89:       Machines.Thermal.convertResistance(
90:           rs*ZReference,
91:           TsSpecification,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/60c0c577a4240961.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
