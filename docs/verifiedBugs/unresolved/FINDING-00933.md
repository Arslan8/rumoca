# FINDING-00933: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.Subtracter |
| Target | feedback.R3 |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-subtracter-feedback-r3-zerolimit.md](../../v2/bugs/FINDING-subtracter-feedback-r3-zerolimit.md) — reviewed as `FINDING-00933-subtracter-feedback-r3.md`, which a later run renamed |
| Original SHA-256 | 8ba8ba5dc09eface36ac68cc9dbb1570a57b7069e782597bab0a7c5eb347850d |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Feedback.mo:8`. Role: `parameter`; binding: `1000`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/OpAmpCircuits/Feedback.mo — source snapshot](../evidence/sources/8767f5f11d8a92ba-Feedback.mo)

```modelica
6:   parameter Real k(final min=0)=1 "Desired amplification";
7:   parameter SI.Resistance R1=1000 "Resistance at inputs of OpAmp";
8:   parameter SI.Resistance R3=R1/k "Calculated resistance to reach desired amplification k";
9:   Basic.Resistor                            r1(final R=R1)
10:     annotation (Placement(transformation(extent={{-10,-10},{10,10}},
11:         origin={-40,70})));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/ab1f9b98b3ad2022.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
