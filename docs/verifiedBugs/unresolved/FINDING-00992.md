# FINDING-00992: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.ShowSaturatingInductor |
| Target | Lnom |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-showsaturatinginductor-lnom-intent.md](../../v2/bugs/FINDING-showsaturatinginductor-lnom-intent.md) — reviewed as `FINDING-00992-showsaturatinginductor-lnom.md`, which a later run renamed |
| Original SHA-256 | 68bc7dcaec02c0a83f9bcc35600cc98c6a867acc74aaed2bb61a6622b6427131 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Examples/ShowSaturatingInductor.mo:6`. Role: `parameter`; binding: `1`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Examples/ShowSaturatingInductor.mo — source snapshot](../evidence/sources/84536af2c7f7a621-ShowSaturatingInductor.mo)

```modelica
4:   extends Modelica.Icons.Example;
5:   parameter SI.Inductance Lzer=2 "Inductance near current=0";
6:   parameter SI.Inductance Lnom=1
7:     "Nominal inductance at Nominal current";
8:   parameter SI.Current Inom=1 "Nominal current";
9:   parameter SI.Inductance Linf=0.5 "Inductance at large currents";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/b3892488197c6c55.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
