# FINDING-02070: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start |
| Target | aims.Lrzero |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-ims-start-aims-lrzero-zerolimit.md](../../v2/bugs/FINDING-ims-start-aims-lrzero-zerolimit.md) — reviewed as `FINDING-02070-ims-start-aims-lrzero.md`, which a later run renamed |
| Original SHA-256 | eed036d81a3ccbd236ba8d0d88ed9f9c149af1af4fd81c1a6100a9d3e338a9a8 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/InductionMachines/IM_SlipRing.mo:34`. Role: `parameter`; binding: `aimsData.Lrzero`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/InductionMachines/IM_SlipRing.mo — source snapshot](../evidence/sources/357d4e0b4a6e5fc4-IM_SlipRing.mo)

```modelica
32:     "Rotor stray inductance per phase w.r.t. rotor side"
33:     annotation (Dialog(tab="Nominal resistances and inductances"));
34:   parameter SI.Inductance Lrzero=Lrsigma
35:     "Rotor zero sequence inductance w.r.t. rotor side"
36:     annotation (Dialog(tab="Nominal resistances and inductances"));
37:   parameter SI.Resistance Rr(start=0.04*ZsRef)
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/2804e4f64ad6a33e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
