# FINDING-00993: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.ShowSaturatingInductor |
| Target | Linf |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-showsaturatinginductor-linf-zerolimit.md](../../v2/bugs/FINDING-showsaturatinginductor-linf-zerolimit.md) — reviewed as `FINDING-00993-showsaturatinginductor-linf.md`, which a later run renamed |
| Original SHA-256 | 131e3962c763f0cfb2ca89889520729027a7c3cb075aa6332730757184ad93cc |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/ShowSaturatingInductor.mo:9`. Role: `parameter`; binding: `0.5`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/ShowSaturatingInductor.mo — source snapshot](../evidence/sources/84536af2c7f7a621-ShowSaturatingInductor.mo)

```modelica
7:     "Nominal inductance at Nominal current";
8:   parameter SI.Current Inom=1 "Nominal current";
9:   parameter SI.Inductance Linf=0.5 "Inductance at large currents";
10:   parameter SI.Voltage U=1.25 "Source voltage (peak)";
11:   parameter SI.Frequency f=1/(2*Modelica.Constants.pi)
12:     "Source frequency";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/b3892488197c6c55.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
