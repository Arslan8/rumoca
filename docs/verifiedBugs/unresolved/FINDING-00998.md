# FINDING-00998: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.ShowSaturatingInductor |
| Target | SaturatingInductance1.Ipar |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-showsaturatinginductor-saturatinginductance1-ipar-divzero-2.md](../../v2/bugs/FINDING-showsaturatinginductor-saturatinginductance1-ipar-divzero-2.md) — reviewed as `FINDING-00998-showsaturatinginductor-saturatinginductance1-ipar.md`, which a later run renamed |
| Original SHA-256 | 2b85f5057dea7deba2232e9cdcbdd3b5192b4bcc5494aaf484f4ee69fc18ed6b |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Basic/SaturatingInductor.mo:19`. Role: `parameter`; binding: `None`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Basic/SaturatingInductor.mo — source snapshot](../evidence/sources/e05b77099ac62435-SaturatingInductor.mo)

```modelica
17:   SI.MagneticFlux Psi "Present flux";
18: protected
19:   parameter SI.Current Ipar(start=Inom/10, fixed=false);
20: initial equation
21:   (Lnom - Linf)/(Lzer - Linf)=Ipar/Inom*(pi/2 - atan(Ipar/Inom));
22: equation
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/b3892488197c6c55.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
