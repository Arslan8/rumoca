# FINDING-00365: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.Lines.CompareLineTrunks |
| Target | z0 |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-comparelinetrunks-z0-intent.md](../../v2/bugs/FINDING-comparelinetrunks-z0-intent.md) — reviewed as `FINDING-00365-comparelinetrunks-z0.md`, which a later run renamed |
| Original SHA-256 | f75bfc17d42c6e7a2ed3de9539fa7f6eb7b331249e3503e45e7813b8c83fba10 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/Lines/CompareLineTrunks.mo:15`. Role: `parameter`; binding: `sqrt((l1 / c1))`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/Lines/CompareLineTrunks.mo — source snapshot](../evidence/sources/7c8809c786a5a457-CompareLineTrunks.mo)

```modelica
13:   parameter SI.Velocity c=1/sqrt(l1*c1) "Speed of EM wave";
14:   parameter SI.Time td=len/c/4 "Transmission delay";
15:   parameter SI.Impedance z0=sqrt(l1/c1) "Characteristic impedance for very high frequency";
16:   Modelica.Blocks.Sources.Ramp ramp(startTime=400e-6, duration=50e-6)
17:     annotation (Placement(transformation(extent={{-88,-10},{-68,10}})));
18:   Modelica.Electrical.Analog.Sources.SignalVoltage srcLump annotation (
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/1ffcf476bae0a4c2.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
