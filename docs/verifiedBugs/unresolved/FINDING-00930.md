# FINDING-00930: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.SignalGenerator |
| Target | VAmp |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-signalgenerator-vamp-divzero-2.md](../../v2/bugs/FINDING-signalgenerator-vamp-divzero-2.md) — reviewed as `FINDING-00930-signalgenerator-vamp.md`, which a later run renamed |
| Original SHA-256 | 0622ce6a20d9754e79e1ce84415ccb927d87290a7c9e414838222834f91d741d |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/SignalGenerator.mo:7`. Role: `parameter`; binding: `10`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/SignalGenerator.mo — source snapshot](../evidence/sources/e994e2cdd2e5a217-SignalGenerator.mo)

```modelica
5:   parameter SI.Voltage Vps=+15 "Positive supply";
6:   parameter SI.Voltage Vns=-Vps "Negative supply";
7:   parameter SI.Voltage VAmp=10 "Desired amplitude of output";
8:   parameter SI.Resistance R1=1000 "Arbitrary resistance for Schmitt trigger part";
9:   parameter SI.Resistance R2=R1*Vps/VAmp "Calculated resistance for Schmitt trigger to reach VAmp";
10:   parameter SI.Frequency f=10 "Desired frequency";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/c8b9183ee19e69f8.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
