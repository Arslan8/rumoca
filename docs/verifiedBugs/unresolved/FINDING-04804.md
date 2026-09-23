# FINDING-04804: Not yet established as a bug or a false positive

| Field | Value |
|---|---|
| Verdict | unresolved |
| Scope / group | baseline-blocked |
| Model | ModelicaTest.Blocks.Continuous_InitialState |
| Target | transferFunction.a |
| Student classification | divisor-reachable-zero |
| Original report | `FINDING-04804-continuous-initialstate-transferfunction-a.md` — [withdrawn](../../v2/bugs/withdrawn.md); a later run no longer makes this claim |
| Original SHA-256 | 4f97e89a8a65429134220fd6fa672dc6c911aa1a3e646f9ae8f7f7bc15da0d44 |

## What remains unresolved

The current Rumoca nominal run is tool-error, before any reported perturbation. This prevents causal attribution to this parameter. Source metadata was recovered, but none of the reviewed source proofs or counterexamples establishes this particular claim. A baseline failure/tool limitation is neither confirmation nor a false positive.

## Source evidence

Compiler/source-resolved declaration: `Blocks/Continuous.mo:1126`. Role: `parameter`; binding: `{1, 1}`; effective min: `None`; effective max: `None`. 

[Blocks/Continuous.mo — source snapshot](../evidence/sources/e0c05b204354b734-Continuous.mo)

```modelica
1124:     parameter Real b[:]={1}
1125:       "Numerator coefficients of transfer function (e.g., 2*s+3 is specified as {2,3})";
1126:     parameter Real a[:]={1}
1127:       "Denominator coefficients of transfer function (e.g., 5*s+6 is specified as {5,6})";
1128:     parameter Modelica.Blocks.Types.Init initType=Modelica.Blocks.Types.Init.NoInit
1129:       "Type of initialization (1: no init, 2: steady state, 3: initial state, 4: initial output)"
```


## Execution evidence

[Rumoca commands, return codes, integrity hashes, bounded output and metadata](../evidence/6eeeef65fb9ae772.json). Baseline: **tool-error**.

No independent runtime override was executed for this target in this audit; this is not a pass.

## Recommended action

Resolve the intended parameter domain and enclosing equations; check inherited bounds, final/protected status, guards and aliases. Construct an otherwise-valid source-level witness, establish a clean baseline in a capable engine, then retranslate at the witness and compare with the runtime override. For equality claims use the actual partner value. Do not apply a blanket min>0 fix yet.

## Scope and limitations

A source-level verdict addresses the reported declaration/claim, not every possible connected system. Tests cover 0–0.5 seconds and are not a proof of long-run stability. Shared instances are not distinct root causes. A missing bound, timeout, compiler error or failed nominal run alone never counts as a verified bug or a false positive. Fixes are proposals; no library/compiler implementation was changed.

[Group and related reports](../groups/baseline-blocked.md) · [Index](../README.md)
