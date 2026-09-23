# FINDING-05052: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | ModelicaTest.Translational.Vehicles |
| Target | vehicleDrag.A |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-vehicles-vehicledrag-a-zerolimit.md](../../v2/bugs/FINDING-vehicles-vehicledrag-a-zerolimit.md) — reviewed as `FINDING-05052-vehicles-vehicledrag-a.md`, which a later run renamed |
| Original SHA-256 | d7771c5cfbdd75f293bd7d68384720cf226edf0e3c12b29c520a44f2648377f4 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Mechanics/Translational/Components/Vehicle.mo:7`. Role: `parameter`; binding: `2.2`; effective min: `None`; effective max: `None`. 

[Mechanics/Translational/Components/Vehicle.mo — source snapshot](../evidence/sources/037334fdb7d77239-Vehicle.mo)

```modelica
5:   parameter SI.Inertia J "Total rotational inertia of drive train";
6:   parameter SI.Length R "Wheel radius";
7:   parameter SI.Area A(start=1) "Cross section of vehicle"
8:     annotation(Dialog(tab="Driving resistances", group="Drag resistance"));
9:   parameter Real Cd(start=0.5) "Drag resistance coefficient"
10:     annotation(Dialog(tab="Driving resistances", group="Drag resistance"));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/e1997bd33cf0ed7f.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
