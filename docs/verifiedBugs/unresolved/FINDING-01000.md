# FINDING-01000: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.ShowSaturatingInductor |
| Target | Inom |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-01000-showsaturatinginductor-inom.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 87d39ea7ff934e2e386a38015c5f099f6bcfe494c05b83d80ede29529bad2a98 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/ShowSaturatingInductor.mo:8`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/ShowSaturatingInductor.mo — source snapshot](../evidence/sources/84536af2c7f7a621-ShowSaturatingInductor.mo)

```modelica
6:   parameter SI.Inductance Lnom=1
7:     "Nominal inductance at Nominal current";
8:   parameter SI.Current Inom=1 "Nominal current";
9:   parameter SI.Inductance Linf=0.5 "Inductance at large currents";
10:   parameter SI.Voltage U=1.25 "Source voltage (peak)";
11:   parameter SI.Frequency f=1/(2*Modelica.Constants.pi)
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/b3892488197c6c55.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
