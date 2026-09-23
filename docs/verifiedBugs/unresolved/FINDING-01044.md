# FINDING-01044: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Electrical.Analog.Examples.ThyristorBehaviourTest |
| Target | thyristor_v4_1.Nbv |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-thyristorbehaviourtest-thyristor-v4-1-nbv-divunresolved.md](../../v2/bugs/FINDING-thyristorbehaviourtest-thyristor-v4-1-nbv-divunresolved.md) — reviewed as `FINDING-01044-thyristorbehaviourtest-thyristor-v4-1-nbv.md`, which a later run renamed |
| Original SHA-256 | d21a3afc24abd134d4f42fee6f5fc747c448607de0b913c1ab66d4b6479b484a |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Electrical/Analog/Semiconductors/Thyristor.mo:19`. Role: `parameter`; binding: `0.74`; effective min: `None`; effective max: `None`. 

[Electrical/Analog/Semiconductors/Thyristor.mo — source snapshot](../evidence/sources/dbc15414032e03ee-Thyristor.mo)

```modelica
17:   parameter SI.Voltage Vt=0.04
18:     "Voltage equivalent of temperature (kT/qn)";
19:   parameter Real Nbv=0.74 "Reverse Breakthrough emission coefficient";
20:  extends Modelica.Electrical.Analog.Interfaces.ConditionalHeatPort;
21:   SI.Current iGK "Gate current";
22:   SI.Voltage vGK "Voltage between gate and cathode";
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/f2dc7c4a18bb2bd2.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
