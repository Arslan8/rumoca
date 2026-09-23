# FINDING-00919: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.OpAmps.SchmittTrigger |
| Target | Vps |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-schmitttrigger-vps-divzero-2.md](../../v2/bugs/FINDING-schmitttrigger-vps-divzero-2.md) — reviewed as `FINDING-00919-schmitttrigger-vps.md`, which a later run renamed |
| Original SHA-256 | a8839a94bf469d57798f650df03f25dc22b5e507feb1a6b68dd5282a8c18e9cb |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/OpAmps/SchmittTrigger.mo:4`. Role: `parameter`; binding: `15`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/OpAmps/SchmittTrigger.mo — source snapshot](../evidence/sources/1146643cdb8f90b2-SchmittTrigger.mo)

```modelica
2: model SchmittTrigger "Schmitt trigger with hysteresis"
3:   extends Modelica.Icons.Example;
4:   parameter SI.Voltage Vps=+15 "Positive supply";
5:   parameter SI.Voltage Vns=-15 "Negative supply";
6:   parameter SI.Voltage Vin=5 "Amplitude of input voltage";
7:   parameter SI.Frequency f=10 "Frequency of input voltage";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/18175c686731491f.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
