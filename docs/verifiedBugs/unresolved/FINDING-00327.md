# FINDING-00327: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.HeatingPNP_NORGate |
| Target | T2.Gbe |
| Student classification | physical-domain-unenforced |
| Original report | [FINDING-heatingpnp-norgate-t2-gbe-zerolimit.md](../../v2/bugs/FINDING-heatingpnp-norgate-t2-gbe-zerolimit.md) — reviewed as `FINDING-00327-heatingpnp-norgate-t2-gbe.md`, which a later run renamed |
| Original SHA-256 | 3025912d8611ee185e97738a2575900850ccde0768bba78140e66f2d788b7b28 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Semiconductors/PNP.mo:17`. Role: `parameter`; binding: `1e-12`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Semiconductors/PNP.mo — source snapshot](../evidence/sources/c83ec9a3404f409f-PNP.mo)

```modelica
15:         parameter Real Mc=0.333 "Base-collector gradation exponent";
16:         parameter SI.Conductance Gbc=1e-15 "Base-collector conductance";
17:         parameter SI.Conductance Gbe=1e-15 "Base-emitter conductance";
18:         parameter Real EMin=-100 "If x < EMin, the exp(x) function is linearized";
19:         parameter Real EMax=40 "If x > EMax, the exp(x) function is linearized";
20:   parameter Boolean useTemperatureDependency = false "= true, if parameters Bf, Br, Is and Vt depend on temperature" annotation(Evaluate=true, HideResult=true, choices(checkBox=true));
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f11c770db9a26ad4.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
