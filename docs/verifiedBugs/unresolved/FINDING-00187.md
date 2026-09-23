# FINDING-00187: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.CompareTransformers |
| Target | R1 |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-comparetransformers-r1-zerolimit.md](../../v2/bugs/FINDING-comparetransformers-r1-zerolimit.md) — reviewed as `FINDING-00187-comparetransformers-r1.md`, which a later run renamed |
| Original SHA-256 | a07de287f8edeed4ca0e5cf2dcd5cdd6c6f3dfffdbc98fcfd89932419cabfed2 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/CompareTransformers.mo:11`. Role: `parameter`; binding: `0.01`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/CompareTransformers.mo — source snapshot](../evidence/sources/d966c9a4658ed8b4-CompareTransformers.mo)

```modelica
9:   parameter SI.Angle phi0=pi/2 "Phase of voltage source";
10:   parameter Real n=2 "Turns ratio primary:secondary voltage";
11:   parameter SI.Resistance R1=0.01
12:     "Primary resistance w.r.t. primary side";
13:   parameter SI.Inductance L1sigma=0.05/(2*pi*f)
14:     "Primary leakage inductance w.r.t. primary side";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/ba392aa660731e79.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
