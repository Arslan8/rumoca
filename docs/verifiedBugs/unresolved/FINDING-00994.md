# FINDING-00994: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.ShowSaturatingInductor |
| Target | SaturatingInductance1.Lnom |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-showsaturatinginductor-saturatinginductance1-lnom-zerolimit.md](../../v2/bugs/FINDING-showsaturatinginductor-saturatinginductance1-lnom-zerolimit.md) — reviewed as `FINDING-00994-showsaturatinginductor-saturatinginductance1-lnom.md`, which a later run renamed |
| Original SHA-256 | 6cd2a4034fe0b57a5aa576ef629e8b126915ae9d4c0386abe5fd2dbe589b1593 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Basic/SaturatingInductor.mo:10`. Role: `parameter`; binding: `Lnom`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Basic/SaturatingInductor.mo — source snapshot](../evidence/sources/e05b77099ac62435-SaturatingInductor.mo)

```modelica
8:   parameter SI.Current Inom(start=1) "Nominal current" annotation(Dialog(
9:     groupImage="modelica://Modelica/Resources/Images/Electrical/Analog/Basic/SaturatingInductor_Lact_i_tight.png"));
10:   parameter SI.Inductance Lnom(start=1)
11:     "Nominal inductance at Nominal current";
12:   parameter SI.Inductance Lzer(start=2*Lnom)
13:     "Inductance near current=0";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/b3892488197c6c55.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
