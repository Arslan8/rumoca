# FINDING-00500: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.Lines.CompareLosslessLines |
| Target | z0 |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-comparelosslesslines-z0-intent.md](../../v2/bugs/FINDING-comparelosslesslines-z0-intent.md) — reviewed as `FINDING-00500-comparelosslesslines-z0.md`, which a later run renamed |
| Original SHA-256 | 015fd094ba93a2646503a546c55748c1dbe6cca1a4f352954c98a068c0be0763 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/Lines/CompareLosslessLines.mo:12`. Role: `parameter`; binding: `sqrt((l / c))`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/Lines/CompareLosslessLines.mo — source snapshot](../evidence/sources/ea6cee3156d3073b-CompareLosslessLines.mo)

```modelica
10:   parameter SI.Velocity c0=1/sqrt(l*c) "Speed of EM wave";
11:   parameter SI.Time td=len/c0 "Transmission delay";
12:   parameter SI.Impedance z0=sqrt(l/c) "Characteristic impedance";
13:   Sources.SignalVoltage source1 annotation (Placement(transformation(
14:         extent={{-10,10},{10,-10}},
15:         rotation=270,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/7d8ac5a7afc90403.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
