# FINDING-01466: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Machines.Examples.DCMachines.DCPM_withLosses |
| Target | dcpmData2.coreParameters.m |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-dcpm-withlosses-dcpmdata2-coreparameters-m-divzero-2.md](../../v2/bugs/FINDING-dcpm-withlosses-dcpmdata2-coreparameters-m-divzero-2.md) — reviewed as `FINDING-01466-dcpm-withlosses-dcpmdata2-coreparameters-m.md`, which a later run renamed |
| Original SHA-256 | c780bc6c3b26d5d097f3719e514931ced222e694c93894fd033b3ab9cf0ef8a6 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Machines/Losses/CoreParameters.mo:4`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Electrical/Machines/Losses/CoreParameters.mo — source snapshot](../evidence/sources/4e22ebe6537d7ba8-CoreParameters.mo)

```modelica
2: record CoreParameters "Parameter record for core losses"
3:   extends Modelica.Icons.Record;
4:   parameter Integer m
5:     "Number of phases (1 for DC, 3 for induction machines)";
6:   parameter SI.Power PRef(min=0) = 0
7:     "Reference core losses at reference inner voltage VRef";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/1255084b3c3934b8.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
