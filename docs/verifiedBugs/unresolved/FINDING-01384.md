# FINDING-01384: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_Start |
| Target | JLoad |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-dcpm-start-jload-zerolimit.md](../../v2/bugs/FINDING-dcpm-start-jload-zerolimit.md) — reviewed as `FINDING-01384-dcpm-start-jload.md`, which a later run renamed |
| Original SHA-256 | 9e642c46a7c68866ec2866b1cd6c565cc82c71ee3cd502c5e23110a69d699e7d |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Examples/DCMachines/DCPM_Start.mo:11`. Role: `parameter`; binding: `0.15`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Examples/DCMachines/DCPM_Start.mo — source snapshot](../evidence/sources/91e45c405eb39058-DCPM_Start.mo)

```modelica
9:   parameter SI.Torque TLoad=63.66 "Nominal load torque";
10:   parameter SI.Time tStep=1.5 "Time of load torque step";
11:   parameter SI.Inertia JLoad=0.15
12:     "Load's moment of inertia";
13:   Machines.BasicMachines.DCMachines.DC_PermanentMagnet dcpm(
14:     VaNominal=dcpmData.VaNominal,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/58aaee5fa3eb7c79.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
