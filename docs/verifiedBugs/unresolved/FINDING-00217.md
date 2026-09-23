# FINDING-00217: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.DemoPowerSupplyWithBuffer |
| Target | f |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-demopowersupplywithbuffer-f-divzero.md](../../v2/bugs/FINDING-demopowersupplywithbuffer-f-divzero.md) — reviewed as `FINDING-00217-demopowersupplywithbuffer-f.md`, which a later run renamed |
| Original SHA-256 | 107c7bd4581df54ebc6a3a25edbfeb959b1e4a7d7f9be63e541b03e32b96f928 |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/DemoPowerSupplyWithBuffer.mo:8`. Role: `parameter`; binding: `1000.0`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/DemoPowerSupplyWithBuffer.mo — source snapshot](../evidence/sources/1b88625d006a439a-DemoPowerSupplyWithBuffer.mo)

```modelica
6:   parameter SI.Current offset = -25 "Pulse current offset";
7:   parameter Real dutyCycle(final min = 0, final max = 1) = 0.5 "Pulse current duty cycle";
8:   parameter SI.Frequency f = 1e3 "Pulse current frequency";
9:   Modelica.Electrical.Analog.Sources.DCPowerSupply dcPowerSupply(
10:     Gcc=0.01,
11:     Rcv=0.01,
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/6b64eb50d329645d.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
