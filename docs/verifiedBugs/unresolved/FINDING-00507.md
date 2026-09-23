# FINDING-00507: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.Lines.SmoothStep |
| Target | Rload |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-smoothstep-rload-zerolimit.md](../../v2/bugs/FINDING-smoothstep-rload-zerolimit.md) — reviewed as `FINDING-00507-smoothstep-rload.md`, which a later run renamed |
| Original SHA-256 | 8729853d8a0907b41d86d36d2a53055c6646ef838c1aac02138f754194ebef56 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/Lines/SmoothStep.mo:6`. Role: `parameter`; binding: `1000`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/Lines/SmoothStep.mo — source snapshot](../evidence/sources/5f3b41af825e9949-SmoothStep.mo)

```modelica
4:   import Modelica.Units.SI;
5:   import Modelica.Constants.small;
6:   parameter SI.Resistance Rload=1000 "Load resistance";
7:   parameter Real r1(final min=small, final unit="Ohm/m")=1e-6 "Resistance per meter";
8:   parameter Real g1(final min=small, final unit="S/m")=1e-12 "Conductance per meter";
9:   parameter Real l1(final min=small, final unit="H/m")=1e-6 "Inductance per meter";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/21f9fcbcb956ec17.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
