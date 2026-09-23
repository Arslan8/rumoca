# FINDING-02071: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.InductionMachines.IMS_Start |
| Target | aims.Rr |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-ims-start-aims-rr-ruleoff.md](../../v2/bugs/FINDING-ims-start-aims-rr-ruleoff.md) — reviewed as `FINDING-02071-ims-start-aims-rr.md`, which a later run renamed |
| Original SHA-256 | c1fd0706f4af7f2be7e4db74a3f3a5569307d30df65f5364a70c0ea384d3934d |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/BasicMachines/InductionMachines/IM_SlipRing.mo:37`. Role: `parameter`; binding: `aimsData.Rr`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/BasicMachines/InductionMachines/IM_SlipRing.mo — source snapshot](../evidence/sources/357d4e0b4a6e5fc4-IM_SlipRing.mo)

```modelica
35:     "Rotor zero sequence inductance w.r.t. rotor side"
36:     annotation (Dialog(tab="Nominal resistances and inductances"));
37:   parameter SI.Resistance Rr(start=0.04*ZsRef)
38:     "Rotor resistance per phase at TRef w.r.t. rotor side"
39:     annotation (Dialog(tab="Nominal resistances and inductances"));
40:   parameter SI.Temperature TrRef(start=293.15)
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/2804e4f64ad6a33e.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
