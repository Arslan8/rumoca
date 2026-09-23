# FINDING-01059: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.Utilities.InverseCapacitor |
| Target | C |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-inversecapacitor-c-zerolimit.md](../../v2/bugs/FINDING-inversecapacitor-c-zerolimit.md) — reviewed as `FINDING-01059-inversecapacitor-c.md`, which a later run renamed |
| Original SHA-256 | 022e2a74b7411d6cfe1b240cb8dfbd93aa8d329a3dc214e45757c33b571f286c |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/Utilities/InverseCapacitor.mo:4`. Role: `parameter`; binding: `1`; effective min: `0`; effective max: `None`. 

[Electrical/Analog/Examples/Utilities/InverseCapacitor.mo — source snapshot](../evidence/sources/1607586cf3eb5c42-InverseCapacitor.mo)

```modelica
2: model InverseCapacitor "Input/output block of an inverse capacitor model"
3:   extends Modelica.Blocks.Icons.Block;
4:   parameter SI.Capacitance C(min=0)=1 "Capacitance";
5:   Modelica.Electrical.Analog.Basic.Capacitor capacitor(C=C, v(fixed=
6:           true, start=0)) annotation (Placement(transformation(
7:         extent={{-10,-10},{10,10}},
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/cdec9ea806a2dbd8.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
