# FINDING-02963: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Polyphase.Examples.TestSensors |
| Target | f |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-testsensors-f-divzero-2.md](../../v2/bugs/FINDING-testsensors-f-divzero-2.md) — reviewed as `FINDING-02963-testsensors-f.md`, which a later run renamed |
| Original SHA-256 | d2c02a3eab372b49d8ef4d29a3856e99af76f7bbdb9c4024c907543d2a987575 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Polyphase/Examples/TestSensors.mo:8`. Role: `parameter`; binding: `50`; effective min: `None`; effective max: `None`. 

[Electrical/Polyphase/Examples/TestSensors.mo — source snapshot](../evidence/sources/a78d8a3449c5ed27-TestSensors.mo)

```modelica
6:   parameter SI.Voltage VRMS=100
7:     "Nominal RMS voltage per phase";
8:   parameter SI.Frequency f=50 "Frequency";
9:   parameter SI.Resistance R=1/sqrt(2) "Load resistance";
10:   parameter SI.Inductance L=1/sqrt(2)/(2*pi*f) "Load inductance";
11:   final parameter SI.Impedance Z=sqrt(R^2 + (2*pi*f*L)^2) "Load impedance";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/d29719876dfb9043.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
