# FINDING-04770: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Thermal.HeatTransfer.Examples.Utilities.DirectCapacity |
| Target | C |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-directcapacity-c-zerolimit.md](../../v2/bugs/FINDING-directcapacity-c-zerolimit.md) — reviewed as `FINDING-04770-directcapacity-c.md`, which a later run renamed |
| Original SHA-256 | 936d2e6811a5b54b8f4633c665efd5955d3ccae7080949bf57267c1ca2cfa928 |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Thermal/HeatTransfer/Examples/Utilities/DirectCapacity.mo:5`. Role: `parameter`; binding: `1`; effective min: `0`; effective max: `None`. 

[Thermal/HeatTransfer/Examples/Utilities/DirectCapacity.mo — source snapshot](../evidence/sources/22834e4a91f39b33-DirectCapacity.mo)

```modelica
3:   "Input/output block of a direct heatCapacity model"
4:   extends Modelica.Blocks.Icons.Block;
5:   parameter SI.HeatCapacity C(min=0)=1 "HeatCapacity";
6:   HeatTransfer.Components.HeatCapacitor heatCapacitor(C=C, T(fixed=true, start=
7:           293.15))
8:     annotation (Placement(transformation(extent={{-20,0},{0,20}})));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/b03b969de523c3de.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
