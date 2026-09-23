# FINDING-00240: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.DifferenceAmplifier |
| Target | Transistor1.Tr.Phic |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-differenceamplifier-transistor1-tr-phic-divzero.md](../../v2/bugs/FINDING-differenceamplifier-transistor1-tr-phic-divzero.md) — reviewed as `FINDING-00240-differenceamplifier-transistor1-tr-phic.md`, which a later run renamed |
| Original SHA-256 | 00df4eb1429ad3c75d016f0b55d613fd832fbfb1ab6dfd69286d2ad6f2f63013 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Semiconductors/NPN.mo:14`. Role: `parameter`; binding: `0.8`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Semiconductors/NPN.mo — source snapshot](../evidence/sources/b1769ee9ceb1f5f0-NPN.mo)

```modelica
12:         parameter SI.Voltage Phie=0.8 "Base-emitter diffusion voltage";
13:         parameter Real Me=0.4 "Base-emitter gradation exponent";
14:         parameter SI.Voltage Phic=0.8 "Base-collector diffusion voltage";
15:         parameter Real Mc=0.333 "Base-collector gradation exponent";
16:         parameter SI.Conductance Gbc=1e-15 "Base-collector conductance";
17:         parameter SI.Conductance Gbe=1e-15 "Base-emitter conductance";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/a3f2f2f9a1ca72bf.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
