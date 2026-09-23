# FINDING-00017: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | Modelica.Clocked.Examples.Systems.Utilities.ComponentsMixingUnit.MixingUnitWithContinuousControl |
| Target | invMixingUnit.tau0 |
| Student classification | divisor-reachable-zero |
| Original report | [FINDING-mixingunitwithcontinuouscontrol-invmixingunit-tau0-divzero-10.md](../../v2/bugs/FINDING-mixingunitwithcontinuouscontrol-invmixingunit-tau0-divzero-10.md) — reviewed as `FINDING-00017-mixingunitwithcontinuouscontrol-invmixingunit-tau0.md`, which a later run renamed |
| Original SHA-256 | 16b19e11bc9c1fc33e30bc889bc41e20677d522ec0023b3a19d5ce1a6d205e1f |

## What remains unresolved

The current Rumoca nominal run is reported-failure, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Clocked/Examples/Systems/Utilities/ComponentsMixingUnit/MixingUnit.mo:23`. Role: `parameter`; binding: `60`; effective min: `None`; effective max: `None`. 

[Clocked/Examples/Systems/Utilities/ComponentsMixingUnit/MixingUnit.mo — source snapshot](../evidence/sources/425e46e253745701-MixingUnit.mo)

```modelica
21:   Real gamma "Reaction speed";
22: protected
23:   parameter SI.Time tau0 = 60;
24:   parameter Real wk0 = k0/c0;
25:   parameter Real weps = eps*T0;
26:   parameter Real wa11 = a1/tau0;
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/4a214d5a5475e994.json). Baseline: **reported-failure**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
