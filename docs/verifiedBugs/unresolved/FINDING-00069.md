# FINDING-00069: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.CauerLowPassSC |
| Target | c5 |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-cauerlowpasssc-c5-zerolimit.md](../../v2/bugs/FINDING-cauerlowpasssc-c5-zerolimit.md) — reviewed as `FINDING-00069-cauerlowpasssc-c5.md`, which a later run renamed |
| Original SHA-256 | 3b9d121b1529390019df322a75bde75fa093afd847e92517bc3120da581c9a35 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/CauerLowPassSC.mo:13`. Role: `parameter`; binding: `0.7262`; effective min: `0`; effective max: `None`. 

[Electrical/Analog/Examples/CauerLowPassSC.mo — source snapshot](../evidence/sources/1f2741d02d1975f9-CauerLowPassSC.mo)

```modelica
11:   parameter SI.Capacitance c4=1/(1.179945^2*l2)
12:     "Filter coefficient c4";
13:   parameter SI.Capacitance c5=0.7262 "Filter coefficient c5";
14:   Modelica.Electrical.Analog.Basic.Capacitor C1(C=c1 + c2,v(start=0, fixed=true))
15:     annotation (Placement(transformation(extent={{-193,30},{-173,50}})));
16:   Modelica.Electrical.Analog.Basic.Capacitor C2(C=c2,v(start=0, fixed=true))
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f208d9a532ab730d.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
