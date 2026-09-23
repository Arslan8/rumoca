# FINDING-03308: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.PowerConverters.Examples.ACDC.RectifierCenterTap2mPulse.DiodeCenterTap2mPulse |
| Target | R |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-diodecentertap2mpulse-r-zerolimit.md](../../v2/bugs/FINDING-diodecentertap2mpulse-r-zerolimit.md) — reviewed as `FINDING-03308-diodecentertap2mpulse-r.md`, which a later run renamed |
| Original SHA-256 | 745f9327631b41843154b46ab4246e4dd4ee119ba66a270485b84ada06c6f01b |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/PowerConverters/Examples/ACDC/RectifierCenterTap2mPulse/DiodeCenterTap2mPulse.mo:9`. Role: `parameter`; binding: `20`; effective min: `None`; effective max: `None`. 

[Electrical/PowerConverters/Examples/ACDC/RectifierCenterTap2mPulse/DiodeCenterTap2mPulse.mo — source snapshot](../evidence/sources/5366caba23a0f5b4-DiodeCenterTap2mPulse.mo)

```modelica
7:   parameter SI.Voltage Vrms=110 "RMS supply voltage";
8:   parameter SI.Frequency f=50 "Frequency";
9:   parameter SI.Resistance R=20 "Load resistance";
10: 
11:   Modelica.Electrical.Analog.Basic.Ground ground annotation (Placement(
12:         transformation(extent={{-90,-100},{-70,-80}})));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/cc51170e18159e7f.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
