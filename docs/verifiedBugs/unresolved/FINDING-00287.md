# FINDING-00287: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.HeatingNPN_NORGate |
| Target | T1.Cje |
| Student classification | physical-bound-permits-zero |
| Original report | [FINDING-heatingnpn-norgate-t1-cje-zerolimit.md](../../v2/bugs/FINDING-heatingnpn-norgate-t1-cje-zerolimit.md) — reviewed as `FINDING-00287-heatingnpn-norgate-t1-cje.md`, which a later run renamed |
| Original SHA-256 | 69cae341e1edbb66e20a9c6f0e95fceb92a8fe2e76681aac435336341f5f57f5 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Semiconductors/NPN.mo:10`. Role: `parameter`; binding: `CapVal`; effective min: `0`; effective max: `None`. 

[Electrical/Analog/Semiconductors/NPN.mo — source snapshot](../evidence/sources/b1769ee9ceb1f5f0-NPN.mo)

```modelica
8:         parameter SI.Time Taur=5e-9 "Ideal reverse transit time";
9:         parameter SI.Capacitance Ccs=1e-12 "Collector-substrate(ground) cap.";
10:         parameter SI.Capacitance Cje=0.4e-12 "Base-emitter zero bias depletion cap.";
11:         parameter SI.Capacitance Cjc=0.5e-12 "Base-coll. zero bias depletion cap.";
12:         parameter SI.Voltage Phie=0.8 "Base-emitter diffusion voltage";
13:         parameter Real Me=0.4 "Base-emitter gradation exponent";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/6cb42ab3dab0120b.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
