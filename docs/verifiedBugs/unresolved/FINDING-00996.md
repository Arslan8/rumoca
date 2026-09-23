# FINDING-00996: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.ShowSaturatingInductor |
| Target | SaturatingInductance1.Linf |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-showsaturatinginductor-saturatinginductance1-linf-zerolimit.md](../../v2/bugs/FINDING-showsaturatinginductor-saturatinginductance1-linf-zerolimit.md) — reviewed as `FINDING-00996-showsaturatinginductor-saturatinginductance1-linf.md`, which a later run renamed |
| Original SHA-256 | f30354565385aa08c861346a09e4b42af6cbfebf5cd7a164f4fcdcf14414be11 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Basic/SaturatingInductor.mo:14`. Role: `parameter`; binding: `Linf`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Basic/SaturatingInductor.mo — source snapshot](../evidence/sources/e05b77099ac62435-SaturatingInductor.mo)

```modelica
12:   parameter SI.Inductance Lzer(start=2*Lnom)
13:     "Inductance near current=0";
14:   parameter SI.Inductance Linf(start=Lnom/2)
15:     "Inductance at large currents";
16:   SI.Inductance Lact(start=Lzer) "Present inductance";
17:   SI.MagneticFlux Psi "Present flux";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/b3892488197c6c55.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
